from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_autoscaling as autoscaling
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_secretsmanager as secretsmanager
from constructs import Construct


class EcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC with 2 AZs, public + private subnets
        vpc = ec2.Vpc(
            self,
            "Vpc",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # ECR repository
        repository = ecr.Repository(
            self,
            "Repository",
            repository_name="merck-devops-api",
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )
        repository.add_lifecycle_rule(max_image_count=10)

        # JWT secret in Secrets Manager
        jwt_secret = secretsmanager.Secret(
            self,
            "JwtSecret",
            secret_name="merck-devops/jwt-secret",
            generate_secret_string=secretsmanager.SecretStringGenerator(
                exclude_punctuation=True,
                password_length=32,
            ),
        )

        # ECS Cluster
        cluster = ecs.Cluster(self, "Cluster", cluster_name="MerckDevOpsStack-Cluster", vpc=vpc)

        # EC2 Auto Scaling Group capacity
        asg = autoscaling.AutoScalingGroup(
            self,
            "Asg",
            vpc=vpc,
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=ecs.EcsOptimizedImage.amazon_linux2(),
            desired_capacity=1,
            min_capacity=1,
            max_capacity=2,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )
        capacity_provider = ecs.AsgCapacityProvider(
            self, "AsgCapacityProvider", auto_scaling_group=asg
        )
        cluster.add_asg_capacity_provider(capacity_provider)

        # Task Definition
        task_definition = ecs.Ec2TaskDefinition(self, "TaskDef")
        container = task_definition.add_container(
            "ApiContainer",
            image=ecs.ContainerImage.from_ecr_repository(repository),
            memory_limit_mib=512,
            cpu=256,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="merck-devops"),
            environment={"ENVIRONMENT": "production"},
            secrets={
                "JWT_SECRET": ecs.Secret.from_secrets_manager(jwt_secret),
            },
        )
        container.add_port_mappings(ecs.PortMapping(container_port=8000, host_port=8000))

        # ALB
        alb = elbv2.ApplicationLoadBalancer(
            self, "Alb", vpc=vpc, internet_facing=True
        )

        # ECS Service
        service = ecs.Ec2Service(
            self,
            "Service",
            service_name="MerckDevOpsStack-Service",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
        )

        # ALB listener and target
        listener = alb.add_listener("Listener", port=80)
        listener.add_targets(
            "EcsTarget",
            port=8000,
            targets=[service],
            health_check=elbv2.HealthCheck(
                path="/health",
                healthy_http_codes="200",
                interval_secs=30,
            ),
        )

        # Security: ALB -> ECS on port 8000 only
        service.connections.allow_from(alb, ec2.Port.tcp(8000), "ALB to ECS")

        # Outputs
        CfnOutput(self, "AlbDns", value=alb.load_balancer_dns_name)
        CfnOutput(self, "EcrUri", value=repository.repository_uri)
