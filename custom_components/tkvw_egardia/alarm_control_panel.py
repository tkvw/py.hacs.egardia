"""Interfaces with Egardia/Woonveilig alarm control panel."""
import logging

import requests

import homeassistant.components.alarm_control_panel as alarm
from homeassistant.components.alarm_control_panel.const import (
    SUPPORT_ALARM_ARM_AWAY,
    SUPPORT_ALARM_ARM_HOME,
)
from homeassistant.const import (
    STATE_ALARM_ARMED_AWAY,
    STATE_ALARM_ARMED_HOME,
    STATE_ALARM_ARMED_NIGHT,
    STATE_ALARM_DISARMED,
    STATE_ALARM_TRIGGERED,
)

from .const import (
    DATA_COORDINATOR,
    DOMAIN_DATA,
    CONF_NAME,
)

from .api.client import Mode

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Egardia Alarm Control Panael platform."""
    if discovery_info is None:
        return

    coordinator = hass.data.get(DOMAIN_DATA)[DATA_COORDINATOR]

    device = EgardiaAlarm(discovery_info.get(CONF_NAME, "Egardia"), coordinator)

    add_entities([device], True)


class EgardiaAlarm(alarm.AlarmControlPanelEntity):
    """Representation of a Egardia alarm."""

    STATES = {
        Mode.Armed: STATE_ALARM_ARMED_AWAY,
        Mode.ArmedHome: STATE_ALARM_ARMED_HOME,
        Mode.Disarmed: STATE_ALARM_DISARMED,
        Mode.Triggered: STATE_ALARM_TRIGGERED,
    }

    def __init__(self, name, coordinator):
        """Initialize the Egardia alarm."""
        self._name = name
        self._coordinator = coordinator
        self._status = None

    async def async_added_to_hass(self):
        """Add Egardiaserver callback if enabled."""
        self.async_on_remove(
            self._coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the device."""

        events = self._coordinator.data.get("events")

        if events is not None and len(events) > 0:
            event = events[0]
            egardia_mode = event.get("mode")
        else:
            status = self._coordinator.data.get("status")
            egardia_mode = status.get("mode")

        return EgardiaAlarm.STATES.get(egardia_mode)

    @property
    def supported_features(self) -> int:
        """Return the list of supported features."""
        return SUPPORT_ALARM_ARM_HOME | SUPPORT_ALARM_ARM_AWAY

    @property
    def should_poll(self):
        """Poll if no report server is enabled."""
        return False

    async def async_update(self):
        """Update the alarm status."""
        await self._coordinator.async_request_refresh()

    async def async_alarm_disarm(self, code=None):
        """Send disarm command."""
        try:
            await self._coordinator.alarm_disarm()
        except Exception as err:
            _LOGGER.error(
                "Egardia device exception occurred when sending disarm command: %s",
                err,
            )

    async def async_alarm_arm_home(self, code=None):
        """Send arm home command."""
        try:
            await self._coordinator.alarm_arm_home()
        except Exception as err:
            _LOGGER.error(
                "Egardia device exception occurred when "
                "sending arm home command: %s",
                err,
            )

    async def async_alarm_arm_away(self, code=None):
        """Send arm away command."""
        try:
            await self._coordinator.alarm_arm()
        except Exception as err:
            _LOGGER.error(
                "Egardia device exception occurred when "
                "sending arm away command: %s",
                err,
            )
