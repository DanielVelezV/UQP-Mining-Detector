from fastapi.routing import APIRouter
from EVE_SSO import refresh_token as rt



sso_token_route = APIRouter(prefix = "/SSO")


@sso_token_route.post("/refresh_token")
async def refresh_token(uuid: str):
    return rt(uuid)