from pydantic import BaseModel



class AuthDataModel(BaseModel):
    Access_Token             : str                           
    Refresh_Access_Token     : str                                   
    Last_Refresh_Milis       : int                               
    Scopes                   : list[str]    
                   

class CorpInfoModel(BaseModel):
    CorpName                 : str                   
    CorpId                   : int               
    Roles                    : list[str]               


class CharDataModel(BaseModel):
    CharHash                 : str                           
    CharName                 : str                               
    CharID                   : int                           
    AuthData                 : AuthDataModel                               
    CorpInfo                 : CorpInfoModel                               

