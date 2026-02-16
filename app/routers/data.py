from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.bearer import get_current_user
from app.auth.jwt_handler import create_access_token
from app.models.auth import TokenRequest, TokenResponse
from app.models.data import DataItem, DataResponse

router = APIRouter(prefix="/api/v1")

DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo"

DUMMY_DATA = [
    DataItem(id=1, name="Widget A", description="High-performance widget", category="widgets"),
    DataItem(id=2, name="Gadget B", description="Multi-purpose gadget", category="gadgets"),
    DataItem(id=3, name="Tool C", description="Precision engineering tool", category="tools"),
]


@router.post("/token", response_model=TokenResponse)
def create_token(request: TokenRequest) -> TokenResponse:
    if request.username != DEMO_USERNAME or request.password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    token = create_access_token(subject=request.username)
    return TokenResponse(access_token=token)


@router.get("/data", response_model=DataResponse)
def get_data(current_user: str = Depends(get_current_user)) -> DataResponse:
    return DataResponse(items=DUMMY_DATA, total=len(DUMMY_DATA))
