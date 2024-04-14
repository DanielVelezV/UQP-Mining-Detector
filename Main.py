from EVE_SSO import create_sso_url, check_state, get_auth, check_token_signature, save_data, refresh_token
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import Routes

app = FastAPI(title = "EVE SSO Auth Programn")

app.include_router(Routes.moons_route)
app.include_router(Routes.sso_token_route)

@app.get("/", include_in_schema = False)
async def read_root():
    
    return RedirectResponse("/docs")

@app.get("/sso")
async def sso(request: Request, code: str, state: str):

    # Checking if the state was the same that is sent. Security Handler
    if not check_state(state):
        return "State not allowed"
    
    response = get_auth(code)

    # Checking the token signature. Security Handler
    contents = check_token_signature(response.json()["access_token"])

    if not contents:
        return "Error decrypting your Auth Code. Communicate with ElWarriorcito"

    # Saving the data

    save_data(contents, response.json())

    return RedirectResponse("https://www.eveonline.com")
