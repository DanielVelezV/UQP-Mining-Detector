from fastapi.routing import APIRouter
import EVE_ESI
import Query
from Models import PydanticModels
from datetime import datetime

war_route = APIRouter(prefix = "/war", tags = ["War"])


@war_route.get("/check_war")
async def check_for_war():

    corp_id = 366498483

    alliance_id = 99010106

    war_found = False

    data = Query.UQPData.get_last_checked_war()

    if data:   

        all_data = []

        corps = EVE_ESI.get_corps_in_alliance(alliance_id)

        last_war = EVE_ESI.get_war_list()

        wars_to_check = last_war[0] - data[0]["war_id"]

        if wars_to_check < 1:
            return "Already checked all wars"

        for x in range(wars_to_check):
            war_to_search = data[0]["war_id"] + x + 1


            war_info = EVE_ESI.get_war_info(war_to_search)

            aggresor = war_info["aggressor"]["alliance_id"] if war_info["aggressor"].get("alliance_id") else war_info["aggressor"]["corporation_id"]

            defensor = war_info["defender"]["alliance_id"] if war_info["defender"].get("alliance_id") else war_info["defender"]["corporation_id"]

            if alliance_id != defensor and alliance_id != aggresor:
                print("Alliance not in war")
            else:
                war_found = True

            if aggresor not in corps and defensor not in corps:
                print("Corp not in war")
            else:
                war_found = True

            war_check = PydanticModels.WarChecker(
                war_id = war_to_search, 
                war_found = war_found,
                corp_id = corp_id,
                alliance_id = alliance_id,
                corps_searched = corps,
                time_checked = datetime.now().strftime("%d-%m-%Y %H:%M:%S %Z")
            )

            all_data.append(war_check)

        Query.UQPData.insert_war_data(all_data)

    return {"War_Found" : war_found}




        
