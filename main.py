from fastapi import BackgroundTasks, FastAPI, HTTPException
from typing import Optional
from utils.client import HeaterClient
from utils import errors, types


app = FastAPI(root_path='/heater')
api = HeaterClient()

async def _set_temp_limit(temp: types.TempData) -> None: await api.set_temp_limit(temp.temp)

@app.get('/actions/power')
async def toggle_power() -> Optional[dict]:
    try:
        await api.toggle_power()
        return {'status': 'ok'}
    except errors.HeaterError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get('/actions/heat')
async def toggle_heat() -> Optional[dict]:
    try:
        await api.toggle_heat()
        return {'status': 'ok'}
    except errors.HeaterError as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post('/set/limit')
async def set_temp_limit(task: BackgroundTasks, temp: types.TempData) -> Optional[dict]:
    if temp.temp == api.status['temp']:
        return {'status': 'ok'}

    if api.limit_running:
        raise HTTPException(status_code=429, detail='Already setting a temperature limit.')
    task.add_task(_set_temp_limit, temp)
    return {'status': 'ok'}
