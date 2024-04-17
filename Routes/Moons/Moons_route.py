from fastapi import APIRouter
import EVE_ESI
import datetime
import Query
from .Moons_data_converter import is_correct

moons_route = APIRouter(prefix = "/Moons", tags = ["Moons"])

# @moons_route.get("/check_moon")
# async def check_moon(UUID: str):
#     response = EVE_ESI.corp_mining_extraction(UUID)

#     arrival_time = datetime.datetime.fromisoformat(response.json()[0]["chunk_arrival_time"]).replace(tzinfo = None)
#     expected_time = datetime.datetime.now()

#     diff = expected_time - arrival_time

#     hours = diff.total_seconds() / 3600

#     threshold = 0.5
        
#     return {
#         "Moon arrival time" : arrival_time.strftime("%d %B %Y %H:%M:%S"),
#         "Moon expected time" : expected_time.strftime("%d %B %Y %H:%M:%S"),
#         "Hours difference" : abs(hours),
#         "Time is correct" : abs(hours) < threshold,
#         "Threshold in hours" : threshold,
#         "Moon Name" : EVE_ESI.get_structure_name(UUID, response.json()[0]["structure_id"])
#     }

@moons_route.get("/refresh_moon_data")   
async def refresh_moon_data(uuid):
     
    user = Query.UQPData.get_user(uuid)

    info = EVE_ESI.corp_mining_extraction(user).json()

    return info


@moons_route.get("/get_all_moons")
async def get_all_moons():

    data = []
    chars = Query.UQPData.get_all_moon_users()

    for x in chars:

        token, isUpdated = EVE_ESI.check_token(x)

        if not isUpdated and not token:
            return False

        response = EVE_ESI.corp_mining_extraction(token)

        arrival_time = response.json()[0]["chunk_arrival_time"]
        extraction_time = response.json()[0]["extraction_start_time"]

        moon_info = EVE_ESI.get_structure_name(token, response.json()[0]["structure_id"])

        is_hour_correct, is_day_correct, moon_cycle, time_between = is_correct(moon_info, arrival_time, extraction_time)

        if is_hour_correct and is_hour_correct and moon_cycle and time_between:
            data.append({
                "Hour Correct" : is_hour_correct,
                "Day Correct" : is_day_correct,
                "Moon Current Cycle" : moon_cycle,
                "Time" : str(time_between)
            })
    

    return data






    

