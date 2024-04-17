from EVE_SSO import get_data, check_token_signature, refresh_token
from jose.exceptions import ExpiredSignatureError, JWTError
import httpx
from fastapi.exceptions import HTTPException
import Query
import time



__BASE_URL = "https://esi.evetech.net/latest/"

def check_token(token):

    if not token:
        print("UUID not found")
        return None, False

    current_time = time.time() 

    latest_update = current_time - token["AuthData"]["Last_Refresh_Milis"]

    if latest_update < 1200:
        print("[UQP-TC] Not expired")
        return token, True

    try:
        print("[UQP-TC] Checking token sig...")
        check_token_signature(token["AuthData"]["Access_Token"])
        return Query.UQPData.get_user(token["CharHash"]), True
    except ExpiredSignatureError:
        refresh_token(token["CharHash"])
        print("[UQP-TC] Token expired. Updating it...")
        return Query.UQPData.get_user(token["CharHash"]), True
    except JWTError as e:
        print("[UQP-TC] Token Error", e.args)
        return None, False

def corp_mining_extraction(token):

    needed_roles = ["Station_Manager"]

    for x in needed_roles:
        if x not in token["CorpInfo"]["Roles"]: return False

    URL = str(__BASE_URL)

    URL += f'corporation/{token["CorpInfo"]["CorpId"]}/mining/extractions/?datasource=tranquility&page=1'

    response = httpx.get(URL, headers = {"Authorization" : f'Bearer {token["AuthData"]["Access_Token"]}'})

    response.raise_for_status()

    return response

def get_corporation_id(char_id, token):
    

    URL = str(__BASE_URL)

    URL += f"characters/{char_id}/corporationhistory/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {token}"})

    response.raise_for_status()

    return response.json()[0]["corporation_id"]
    
def get_corp_info(corp_id):

    URL = str(__BASE_URL)

    URL += f"corporations/{corp_id}/?datasource=tranquility"

    response = httpx.get(URL)

    response.raise_for_status()

    return response.json()

def check_roles(uuid, roles: list[str]):

    char_roles = get_roles(uuid)

    current_roles = [x for x in roles if x in char_roles["roles"]]

    if current_roles != roles:
        return False
    
    return True

def get_roles(char_id, token):
    
    URL = str(__BASE_URL)

    URL += f"characters/{char_id}/roles/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f"Bearer {token}"})

    response.raise_for_status()

    return response.json()

def get_structure_name(token, struc_id) -> str: 
    
    URL = str(__BASE_URL)

    URL += f"universe/structures/{struc_id}/?datasource=tranquility"

    response = httpx.get(URL, headers = {"Authorization" : f'Bearer {token["AuthData"]["Access_Token"]}'})

    response.raise_for_status()

    return response.json()["name"]




