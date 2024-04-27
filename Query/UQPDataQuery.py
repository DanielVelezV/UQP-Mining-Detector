from Db.Conn.Connection import client, DB, UQPDC, UQPWarC
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

    #region War
    @staticmethod
    def get_last_checked_war():
        data = UQPWarC.find().limit(1).sort([('$natural',-1)])

        return data

    @staticmethod
    def insert_war_data(wars: list[WarChecker]):
        
        models = [x.model_dump() for x in wars]

        data = UQPWarC.insert_many(models)

        return data

    #endregion

