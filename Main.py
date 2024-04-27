from EVE_SSO import create_sso_url, check_state, get_auth, check_token_signature, save_data, refresh_token
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import Routes
import Query
from Models import PydanticModels as Models
import EVE_ESI
import time

app = FastAPI(title = "EVE SSO Auth Programn")

app.include_router(Routes.moons_route)
app.include_router(Routes.sso_token_route)
app.include_router(Routes.war_route)

@app.get("/", include_in_schema = False)
async def read_root():
    
    return RedirectResponse("/docs")

@app.get("/sso")
async def sso(request: Request, code: str, state: str):

    # Checking if the state was the same that is sent. Security Handler
    if not check_state(state):
        return "State not allowed"
    
    try:

        auth = Models.CharAUth.model_validate(get_auth(code).json())

        # Checking the token signature. Security Handler
        contents = Models.CharDecryptedAuth.model_validate(check_token_signature(auth.access_token))
    except:
        return {"Error" : "There was an erro parsing the data"}
    
    roles = []

    if "esi-characters.read_corporation_roles.v1" in contents.scp:
        roles = EVE_ESI.get_roles(contents.sub.split(":")[2], auth.access_token)["roles"]


    corp_id  = EVE_ESI.get_corporation_id(contents.sub.split(":")[2], auth.access_token)

    corp_info = EVE_ESI.get_corp_info(corp_id)

    playerModel = Models.CharDataModel(
        CharHash = contents.owner,
        CharName = contents.name,
        CharID = contents.sub.split(":")[2],
        AuthData = Models.AuthDataModel(
            Access_Token = auth.access_token,
            Refresh_Access_Token = auth.refresh_token,
            Last_Refresh_Milis = round(time.time()),
            Scopes = contents.scp
        ),
        CorpInfo = Models.CorpInfoModel(
            CorpId = corp_id,
            CorpName = corp_info["name"],
            Roles = roles
        )
    )
    
    Query.UQPData.insert_user(playerModel)
    
    return RedirectResponse("https://www.eveonline.com")
