from ENV_HANDLER import CLIENT_ID, SECRET_KEY, REDIRECT_URI, STATE
import secrets
import httpx
import base64
from jose import jwt
import json
import Query
from Models.PydanticModels import *
import time

# Scopes that will be requested on player login
current_scopes = ["esi-mail.read_mail.v1", "esi-universe.read_structures.v1", "esi-characters.read_corporation_roles.v1", "esi-industry.read_corporation_mining.v1"]


# SSO URL. Used to register new users
def create_sso_url():

    __base_url = "https://login.eveonline.com/v2/oauth/authorize/?"

    __base_url += "response_type=code&"

    __base_url += f"redirect_uri={REDIRECT_URI}&"

    __base_url += f"client_id={CLIENT_ID}&"

    __base_url += f"state={STATE}&"

    __base_url += f"scope={'%20'.join(current_scopes)}"

    return __base_url

# Easy check. Checking if the state sent in the SSO Url is the same received by the server.
def check_state(state) -> bool:
    return state == STATE

# Generate the Auth code. This is a bearer token to use in the ESI
def get_auth(code, garant_type = "authorization_code"):


    # Base URL of EVE Auth Servers
    __base_url = "https://login.eveonline.com/v2/oauth/token"
    
    # B64 Encoding string required. Ref: https://docs.esi.evetech.net/docs/sso/web_based_sso_flow.html

    encoded_string = f"{CLIENT_ID}:{SECRET_KEY}"

    encoded_string = encoded_string.encode("ascii")

    encoded_string_bytes = base64.b64encode(encoded_string)

    base_64_string = encoded_string_bytes.decode("ascii")

    if garant_type == "authorization_code":
        params = {
            "grant_type": garant_type,
            "code": code
        }
    elif garant_type == "refresh_token":
        params = {
            "grant_type": garant_type,
            "refresh_token": code
        }


    params = url_encode(params)

    # Requests to the Auth servers to get the token
    response = httpx.post(__base_url, headers = {
        "Authorization" : f"Basic {base_64_string}",
        "Content-Type" : "application/x-www-form-urlencoded",
        "Host": "login.eveonline.com"
    }, data = params)

    # Check for errors
    response.raise_for_status()

    return response

# Encode URL params
def url_encode(params):
    
    return "&".join(f"{key}={value}" for key, value in params.items())

# Used to save data into the data.json. data.json is in .gitignore to protect the data
def save_data(decrypted_jwt, jwt):

    # Data saving for chars. 
    # TODO: Move everything to a Non-Relational Database


    data = json.load(open("data.json"))

    if decrypted_jwt["owner"] not in data["Chars"]:
        data["Chars"][decrypted_jwt["owner"]] = {}
        data["Chars"][decrypted_jwt["owner"]] = {
            "name": decrypted_jwt["name"],
            "char_id" : decrypted_jwt["sub"].split(":")[2],
            "access_token" : jwt["access_token"],
            "refresh_access_token" : jwt["refresh_token"]
        }
        json.dump(data, open("data.json", "w"), indent = 4)

        return True
    else:

        data["Chars"][decrypted_jwt["owner"]] = {}
        data["Chars"][decrypted_jwt["owner"]] = {
            "name": decrypted_jwt["name"],
            "char_id" : decrypted_jwt["sub"].split(":")[2],
            "access_token" : jwt["access_token"],
            "refresh_access_token" : jwt["refresh_token"]
        }

        json.dump(data, open("data.json", "w"), indent = 4)

        return False

# Checking the token signature with Eve servers. Used to decrypt the bearer token that we previously obtained
def check_token_signature(token):

    # Method to check the signature of the obtained token. 
    # Basically this decrypts the token to get the necessary data from the player to make the relations in the database.
    
    # JSON Web Keys
    JWK_ALGORITHM = "RS256"
    JWK_ISSUERS = ("login.eveonline.com", "https://login.eveonline.com")
    JWK_AUDIENCE = "EVE Online"

    # Auth server for EVE
    SSO_META_DATA_URL = "https://login.eveonline.com/.well-known/oauth-authorization-server"

    response = httpx.get(SSO_META_DATA_URL)

    response.raise_for_status()

    jwk_uris = response.json()["jwks_uri"]

    response = httpx.get(jwk_uris)

    response.raise_for_status()

    jwt_sets = response.json()["keys"]

    jwk_set = [key for key in jwt_sets if key["alg"] == JWK_ALGORITHM].pop()

    # Decode token

    contents = jwt.decode(
        token = token,
        key = jwk_set,
        algorithms = JWK_ALGORITHM,
        issuer = JWK_ISSUERS,
        audience = JWK_AUDIENCE
    )

    return contents

# Get data from the data.json using the hashId for the player.
def get_data(uuid: str):
    data = json.load(open("data.json"))

    if uuid not in data["Chars"]:
        return None
    
    return data["Chars"][uuid]

# Used to refresh the token for the player.
def refresh_token(char_hash):

    data = Query.UQPData.get_user(char_hash)

    if not data:
        return False

    auth = CharAUth.model_validate(get_auth(data["AuthData"]["Refresh_Access_Token"], "refresh_token").json())

    contents = CharDecryptedAuth.model_validate(check_token_signature(auth.access_token))

    if not contents:
        return False

    # Saving the data

    AuthData = AuthDataModel(
            Access_Token = auth.access_token,
            Refresh_Access_Token = auth.refresh_token,
            Last_Refresh_Milis = round(time.time()),
            Scopes = contents.scp
        )
    
    return Query.UQPData.update_token(char_hash, AuthData)

