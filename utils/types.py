from pydantic import BaseModel


class TempData(BaseModel):
    temp: int


class TimerData(BaseModel):
    hours: int
