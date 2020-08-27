"""
Custom integration to integrate blueprint with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom-components/blueprint
"""
import asyncio
from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers import discovery

from .api.client import Client, Gate03
from .coordinator import EgardiaCoordinator

from .const import (
    CONF_INTERVAL_DISARMED,
    CONF_INTERVAL_ARMED,
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_DEVICE,
    DATA_COORDINATOR,
    DEFAULT_INTERVAL_DISARMED,
    DEFAULT_INTERVAL_ARMED,
    DEFAULT_DEVICE,
    DOMAIN,
    DOMAIN_DATA,
    PLATFORMS,
    STARTUP_MESSAGE,
)

_LOGGER = logging.getLogger(__name__)

DEVICES = {"GATE-03": Gate03()}


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    if (hass.data.get(DOMAIN_DATA)) is None:
        hass.data.setdefault(DOMAIN_DATA, {})
        _LOGGER.info(STARTUP_MESSAGE)

    conf = config[DOMAIN]

    interval_armed = conf.get(CONF_INTERVAL_ARMED, DEFAULT_INTERVAL_ARMED)
    interval_disarmed = conf.get(CONF_INTERVAL_DISARMED, DEFAULT_INTERVAL_DISARMED)
    hostname = conf.get(CONF_HOSTNAME)
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    device = conf.get(CONF_DEVICE, DEFAULT_DEVICE)

    api = Client(
        hostname, username, password, DEVICES.get(device, DEVICES.get(DEFAULT_DEVICE))
    )

    coordinator = EgardiaCoordinator(hass, api, interval_armed, interval_disarmed)

    await coordinator.async_refresh()

    hass.data.get(DOMAIN_DATA)[DATA_COORDINATOR] = coordinator

    await discovery.async_load_platform(
        hass, "alarm_control_panel", DOMAIN, conf, config
    )

    return True


# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Set up this integration using UI."""
#     if hass.data.get(DOMAIN) is None:
#         hass.data.setdefault(DOMAIN, {})
#         _LOGGER.info(STARTUP_MESSAGE)

#     interval = entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL)
#     hostname = entry.data.get(CONF_HOSTNAME)
#     username = entry.data.get(CONF_USERNAME)
#     password = entry.data.get(CONF_PASSWORD)

#     coordinator = WoonveiligDataUpdateCoordinator(
#         hass, interval=interval, hostname=hostname, username=username, password=password
#     )
#     await coordinator.async_refresh()

#     if not coordinator.last_update_success:
#         raise ConfigEntryNotReady

#     hass.data[DOMAIN][entry.entry_id] = coordinator

#     for platform in PLATFORMS:
#         if entry.options.get(platform, True):
#             coordinator.platforms.append(platform)
#             hass.async_add_job(
#                 hass.config_entries.async_forward_entry_setup(entry, platform)
#             )

#     entry.add_update_listener(async_reload_entry)
#     return True

# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Handle removal of an entry."""
#     coordinator = hass.data[DOMAIN][entry.entry_id]
#     unloaded = all(
#         await asyncio.gather(
#             *[
#                 hass.config_entries.async_forward_entry_unload(entry, platform)
#                 for platform in PLATFORMS
#                 if platform in coordinator.platforms
#             ]
#         )
#     )
#     if unloaded:
#         hass.data[DOMAIN].pop(entry.entry_id)

#     return unloaded


# async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
#     """Reload config entry."""
#     await async_unload_entry(hass, entry)
#     await async_setup_entry(hass, entry)
