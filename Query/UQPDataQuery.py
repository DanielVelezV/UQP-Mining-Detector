from Db.Conn.Connection import client, DB, UQPDC
from Models.PydanticModels import *




class UQPData():


    @staticmethod
    def insert_user(user: CharDataModel):

        replaced = UQPDC.replace_one({"CharHash" : user.CharHash}, user.model_dump(), upsert = True)

        # inserted =  UQPDC.insert_one(user.model_dump())

    @staticmethod
    def get_user(char_hash):

        data = UQPDC.find_one({"CharHash" : char_hash})
        
        if data:
            data.pop("_id")
        else:
            return None

        return data

    #region AuthData
    @staticmethod
    def update_token(char_hash, auth_data: AuthDataModel):

        data = UQPDC.update_one({"CharHash" : char_hash}, {
            "$set" : {"AuthData" : auth_data.model_dump()}
        })

        return data.modified_count
    #endregion

    #region Moons
    @staticmethod
    def get_all_moon_users():
        data = UQPDC.find({"CorpInfo.Roles" : "Station_Manager" })

        return data

    #endregion

