from enum import Enum
from typing import TypedDict, List

import aiohttp


class Mode(Enum):
    Disarmed = 0
    Armed = 1
    ArmedHome = 2
    Triggered = 10
    TriggeredPanic = 20
    DisarmedPanic = 21
    Unset = 99


class BatteryLevel(Enum):
    Ok = 0
    Low = 1
    Critical = 2
    Dead = 3


class AlarmStatus(TypedDict):
    mode: Mode
    battery: BatteryLevel


class EgardiaDevice(TypedDict):
    name: str
    battery: BatteryLevel


class EgardiaEvent(TypedDict):
    mode: Mode
    msg: str


class Client:
    def __init__(self, hostname, username, password, device: EgardiaDevice):
        self._hostname = hostname
        self._username = username
        self._password = password
        self._device = device

    async def get_devices(self):
        return await self._device.get_devices(self)

    async def get_status(self):
        return await self._device.get_status(self)

    async def get_events(self):
        return await self._device.get_events(self)

    async def set_status(self, mode: Mode, area: str = "1"):
        return await self._device.set_status(self, mode, area)


class EgardiaGateway:
    def __init__(self, model: str):
        self.model = model

    async def get_devices(self, client: Client) -> List[EgardiaDevice]:
        pass

    async def get_status(self, client: Client) -> AlarmStatus:
        pass

    async def get_events(self, client: Client) -> List[EgardiaEvent]:
        pass

    async def set_status(self, client: Client, mode: Mode, area: str = "1"):
        pass


class Gate03(EgardiaGateway):
    STATUS = {
        "Full Arm": Mode.Armed,
        "Disarm": Mode.Disarmed,
        "Home Arm 1": Mode.ArmedHome,
        "Unset": Mode.Unset,
    }

    def __init__(self):
        super().__init__("GATE-03")

    async def get_devices(self, client: Client) -> List[EgardiaDevice]:
        data = await self.get(client, "deviceListGet")
        return data["senrows"]

    async def get_status(self, client: Client) -> AlarmStatus:
        data = await self.get(client, "panelCondGet")
        updates = data.get("updates", {})
        mode = Gate03.STATUS[updates.get("mode_a1")]
        return {"mode": mode, "battery": BatteryLevel.Ok}

    def transform_event(self, record):
        mode = Mode.Unset
        if record.get('mode'):
            mode = Gate03.STATUS[record.get("mode")]
        msg = record.get("msg")

        if "Burglar Alarm".casefold() == msg.casefold():
            mode = Mode.Triggered
        elif "Panic Alarm".casefold() == msg.casefold():
            mode = Mode.TriggeredPanic
        elif "Disarm Self Panic".casefold() == msg.casefold():
            mode = Mode.DisarmedPanic

        return {"mode": mode, "msg": msg}

    async def get_events(self, client: Client) -> List[EgardiaEvent]:
        data = await self.get(client, "logsGet")
        rows = [
            event
            for event in data.get("logrows", [])
            if event.get("mode") is not None or event.get("msg") == "Disarm Self Panic"
        ]
        return list(map(self.transform_event, rows))

    async def set_status(self, client: Client, mode: Mode, area: str = "1"):
        return await self.post(
            client, "panelCondPost", {"area": area, "mode": mode.value}
        )

    async def get(self, client: Client, action: str):
        async with self.create_session(client) as session:
            async with session.get(self.endpoint(client, action)) as response:
                return await response.json(content_type=None)

    async def post(self, client: Client, action: str, data):
        async with self.create_session(client) as session:
            async with session.post(
                self.endpoint(client, action), data=data
            ) as response:
                return await response.json(content_type=None)

    def endpoint(self, client: Client, action: str):
        return f"http://{client._hostname}/action/{action}"

    def create_session(self, client: Client):
        return aiohttp.ClientSession(
            auth=aiohttp.BasicAuth(client._username, client._password),
            timeout=aiohttp.ClientTimeout(total=5),
        )