from pydantic import BaseModel




class WarChecker(BaseModel):
    war_id                  : int
    war_found               : bool
    time_checked            : str
    corp_id                 : int
    alliance_id             : int
    corps_searched          : list[int]

