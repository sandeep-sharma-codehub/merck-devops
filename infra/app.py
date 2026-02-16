#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.ecs_stack import EcsStack

app = cdk.App()
EcsStack(app, "MerckDevOpsStack")
app.synth()
