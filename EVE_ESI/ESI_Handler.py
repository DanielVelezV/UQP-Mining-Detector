from EVE_SSO import get_data, check_token_signature, refresh_token
from jose.exceptions import ExpiredSignatureError, JWTError
import httpx
from fastapi.exceptions import HTTPException


__BASE_URL = "https://esi.evetech.net/latest/"

def __check_token(uuid):

    token = get_data(uuid)

    if not token:
        print("UUID not found.")
        return False

    try:
        print("Checking token signature...")
        check_token_signature(token["access_token"])
        return True
    except ExpiredSignatureError:
        refresh_token(uuid)
        print("Token expired. Updating it...")
        return True
    except JWTError as e:
        print("JWT Error", e.args)
        return False

def corp_mining_extraction(uuid):

    isTokenValid = __check_token(uuid)

    needed_roles = ["Station_Manager"]

    if not isTokenValid:
        raise HTTPException(detail = "Invalid token")
    
    if not check_roles(uuid, needed_roles):
        raise HTTPException(detail = f"You need corp roles: {needed_roles}")
    
    data = get_data(uuid)

    corp_id = get_corporation_id(uuid)

    URL = str(__BASE_URL)

    URL += f"corporation/{corp_id}/mining/extractions/?datasource=tranquility&page=1"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {data['access_token']}"})

    response.raise_for_status()

    return response

def get_corporation_id(uuid):
    
    data = get_data(uuid)

    URL = str(__BASE_URL)

    URL += f"characters/{data['char_id']}/corporationhistory/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {data['access_token']}"})

    response.raise_for_status()

    return response.json()[0]["corporation_id"]
    
def check_roles(uuid, roles: list[str]):

    char_roles = get_roles(uuid)

    current_roles = [x for x in roles if x in char_roles["roles"]]

    if current_roles != roles:
        return False
    
    return True

def get_roles(uuid):
    
    data = get_data(uuid)
    
    URL = str(__BASE_URL)

    URL += f"characters/{data['char_id']}/roles/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {data['access_token']}"})

    response.raise_for_status()

    return response.json()

def get_structure_name(uuid, struc_id) -> str:

    data = get_data(uuid)
    
    URL = str(__BASE_URL)

    URL += f"universe/structures/{struc_id}/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {data['access_token']}"})

    response.raise_for_status()

    return response.json()["name"]




