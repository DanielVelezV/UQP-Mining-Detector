from fastapi.routing import APIRouter
from EVE_SSO import refresh_token as rt



sso_token = APIRouter(prefix = "/SSO")


@sso_token.post("/refresh_token", include_in_schema = False)
async def refresh_token(id: str):
    return rt(id)