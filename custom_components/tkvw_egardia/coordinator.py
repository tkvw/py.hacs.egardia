from datetime import timedelta, datetime, timezone
import asyncio
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN
from .api.client import Mode

_LOGGER = logging.getLogger(__name__)


class EgardiaCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass, api, interval_armed, interval_disarmed):
        """Initialize."""
        self.api = api
        self.counter = 0
        self.interval_armed = timedelta(seconds=interval_armed)
        self.interval_disarmed = timedelta(seconds=interval_disarmed)

        super().__init__(
            hass, _LOGGER, name=DOMAIN, update_interval=self.interval_armed
        )

    async def alarm_disarm(self):
        return await self.set_status(Mode.Disarmed)

    async def alarm_arm(self):
        return await self.set_status(Mode.Armed)

    async def alarm_arm_home(self):
        return await self.set_status(Mode.ArmedHome)

    async def set_status(self, mode: Mode):
        result = await self.api.set_status(mode)
        await self.async_refresh()
        return result

    async def get_devices(self):
        if self.data is None or self.data.get("devices") is None:
            return await self.api.get_devices()

        return self.data.get("devices")

    async def get_events(self):
        return await self.api.get_events()

    async def get_status(self):
        return await self.api.get_status()

    async def _async_update_data(self):
        """Update data via library."""
        try:
            self.counter += 1
            devices, events, status = await asyncio.gather(
                self.get_devices(), self.get_events(), self.get_status()
            )

            if status.get("mode") == Mode.Disarmed:
                self.update_interval = self.interval_disarmed
            else:
                self.update_interval = self.interval_armed

            return {
                "timestamp": datetime.now(timezone.utc),
                "devices": devices,
                "events": events,
                "status": status,
            }
        except Exception as exception:
            raise UpdateFailed(exception)
