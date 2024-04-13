from EVE_SSO import create_sso_url, check_state, get_auth, check_token_signature, save_data
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


app = FastAPI(title = "EVE SSO Auth Programn")

@app.get("/", include_in_schema = False)
async def read_root():
    
    return RedirectResponse("/docs")


@app.get("/sso")
async def sso(request: Request, code: str, state: str):

    # Checking if the state was the same that is sent. Security Handler
    if not check_state(state):
        return "State not allowed"
    
    response = get_auth(code)

    if response.status_code != 200:
        return "Error getting data. Communicate with ElWarriorcito"


    # Checking the token signature. Security Handler
    contents = check_token_signature(response.json()["access_token"])

    if not contents:
        return "Error decrypting your Auth Code. Communicate with ElWarriorcito"

    # Saving the data

    save_data(contents, response.json())

    return RedirectResponse("https://www.eveonline.com")






