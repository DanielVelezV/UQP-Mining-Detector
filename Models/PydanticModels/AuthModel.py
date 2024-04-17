from pydantic import BaseModel, ConfigDict



class CharAUth(BaseModel):

    model_config = ConfigDict(strict=True)

    access_token            : str              
    refresh_token           : str          

class CharDecryptedAuth(BaseModel):

    model_config = ConfigDict(strict=True)

    sub                     : str
    scp                     : list[str]             
    owner                   : str                 
    name                    : str                 
