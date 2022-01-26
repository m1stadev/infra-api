from utils import errors

import asyncio

KEYS = {
    'power': 'KEY_POWER',
    'heat': 'KEY_MODE',
    'oscillate': 'KEY_MOVE',
    'timer': 'KEY_TIMER',
    'increase': 'KEY_UP',
    'decrease': 'KEY_DOWN'
}

class HeaterClient:
    def __init__(self):
        self.status = {
            'enabled': False, # Heater client is expected to be initiated with the power off.
            'high_heat': True,
            'temp': 75
        }

        self.limit_running = False

    async def _send_cmd(self, code: str) -> bool:
        args = (
            'irsend',
            'SEND_ONCE',
            'heater',
            KEYS[code]
        )

        cmd = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.STDOUT)
        return await cmd.wait() == 0
    
    async def toggle_power(self) -> None: 
        cmd = await self._send_cmd('power')
        await asyncio.sleep(1)

        if cmd == True:
            self.status['enabled'] = not self.status['enabled']

            if self.status['enabled'] == False: # Reset values to default once powered off
                self.status['high_heat'] = True
                self.status['temp'] = 75

        else:
            raise errors.HeaterError(f"Failed to turn heater {'on' if self.status['enabled'] == False else 'off'}.")

    async def toggle_heat(self) -> None:
        cmd = await self._send_cmd('heat')
        if cmd == False:
            raise errors.HeaterError(f"Failed to set high heat {'on' if self.status['high_heat'] == False else 'off'}.")
    
        self.status['high_heat'] = not self.status['high_heat']
        await asyncio.sleep(1)

    async def set_temp_limit(self, temp: int) -> None:
        self.limit_running = True
        if not 41 <= temp <= 90:
            raise ValueError('Temperature limit must be between 41°F-90°F.')

        if temp > self.status['temp']:
            increase = temp - self.status['temp'] + 1
            for _ in range(increase):
                if await self._send_cmd('increase') == False:
                    raise errors.HeaterError('Failed to raise temperature limit.')

                await asyncio.sleep(0.5)

        else:
            decrease = self.status['temp'] + 1 - temp
            for _ in range(decrease):
                if await self._send_cmd('decrease') == False:
                    raise errors.HeaterError('Failed to lower temperature limit.')

                await asyncio.sleep(0.5)

        self.status['temp'] = temp
        await asyncio.sleep(5)
        self.limit_running = False
