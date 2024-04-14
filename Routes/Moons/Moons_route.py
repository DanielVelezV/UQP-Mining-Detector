from fastapi import APIRouter
import EVE_ESI
import datetime


moons_route = APIRouter(prefix = "/Moons", tags = ["Moons"])

# TODO
# Move data to non-relational database

roles_needed_for_route = ["Station_Manager"]

@moons_route.get("/check_moon")
async def check_moon(UUID: str):
    response = EVE_ESI.corp_mining_extraction(UUID)

    arrival_time = datetime.datetime.fromisoformat(response.json()[0]["chunk_arrival_time"]).replace(tzinfo = None)
    expected_time = datetime.datetime.now()

    diff = expected_time - arrival_time

    hours = diff.total_seconds() / 3600

    threshold = 0.5
        
    return {
        "Moon arrival time" : arrival_time.strftime("%d %B %Y %H:%M:%S"),
        "Moon expected time" : expected_time.strftime("%d %B %Y %H:%M:%S"),
        "Hours difference" : abs(hours),
        "Time is correct" : abs(hours) < threshold,
        "Threshold in hours" : threshold,
        "Moon Name" : EVE_ESI.get_structure_name(UUID, response.json()[0]["structure_id"])
    }

    
    