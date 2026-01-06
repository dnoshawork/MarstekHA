"""The Marstek Venus E 3.0 integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_SCAN_INTERVAL
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import device_registry as dr
import voluptuous as vol

from .const import DOMAIN, CONF_IP_ADDRESS, CONF_PORT, DEFAULT_PORT, DEFAULT_SCAN_INTERVAL
from .coordinator import MarstekVenusE3Coordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

# Days of week mapping for conversion
WEEKDAY_TO_BIT = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def convert_days_to_bitmap(days: list[str]) -> int:
    """Convert list of day names to bitmap.

    Args:
        days: List of day names (e.g., ["monday", "friday"])

    Returns:
        Bitmap integer (0-127)
    """
    bitmap = 0
    for day in days:
        day_lower = day.lower()
        if day_lower in WEEKDAY_TO_BIT:
            bitmap |= (1 << WEEKDAY_TO_BIT[day_lower])
    return bitmap


# Service schema
SERVICE_SET_MODE_SCHEMA = vol.Schema(
    {
        vol.Required("device_id"): str,
        vol.Required("mode"): vol.In(["0", "1", "2", "3"]),
        vol.Optional("start_time"): str,
        vol.Optional("end_time"): str,
        vol.Optional("days"): [str],
        vol.Optional("week_set", default=127): vol.All(int, vol.Range(min=0, max=127)),
        vol.Optional("power", default=0): vol.All(int, vol.Range(min=-3000, max=3000)),
        vol.Optional("enable", default=1): vol.All(int, vol.Range(min=0, max=1)),
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Marstek Venus E 3.0 from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get configuration
    ip_address = entry.data[CONF_IP_ADDRESS]
    port = entry.options.get(
        CONF_PORT,
        entry.data.get(CONF_PORT, DEFAULT_PORT),
    )
    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    # Create coordinator
    coordinator = MarstekVenusE3Coordinator(
        hass,
        ip_address,
        port,
        scan_interval,
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Setup platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Setup options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # Register services
    async def async_set_mode_service(call: ServiceCall) -> None:
        """Handle the set_mode service call."""
        device_id = call.data["device_id"]
        mode = int(call.data["mode"])
        start_time = call.data.get("start_time")
        end_time = call.data.get("end_time")

        # Support 'days' field (priority) or 'week_set' (backward compatibility)
        days = call.data.get("days")
        if days:
            week_set = convert_days_to_bitmap(days)
            _LOGGER.debug("Converted days %s to bitmap %d", days, week_set)
        else:
            week_set = call.data.get("week_set", 127)
            _LOGGER.debug("Using legacy week_set bitmap: %d", week_set)

        power = call.data.get("power", 0)
        enable = call.data.get("enable", 1)

        # Find the coordinator for this device
        device_registry = dr.async_get(hass)
        device = device_registry.async_get(device_id)

        if not device:
            _LOGGER.error("Device %s not found", device_id)
            return

        # Find the config entry for this device
        coordinator_entry_id = None
        for entry_id in device.config_entries:
            if entry_id in hass.data[DOMAIN]:
                coordinator_entry_id = entry_id
                break

        if not coordinator_entry_id:
            _LOGGER.error("Coordinator not found for device %s", device_id)
            return

        coordinator = hass.data[DOMAIN][coordinator_entry_id]

        # Call the set_mode method
        success = await coordinator.async_set_mode(
            mode=mode,
            start_time=start_time,
            end_time=end_time,
            week_set=week_set,
            power=power,
            enable=enable,
        )

        if success:
            _LOGGER.info("Successfully set mode to %s", mode)
            # Force update to get new state
            await coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to set mode to %s", mode)

    # Register the service only once (for the first entry)
    if not hass.services.has_service(DOMAIN, "set_mode"):
        hass.services.async_register(
            DOMAIN,
            "set_mode",
            async_set_mode_service,
            schema=SERVICE_SET_MODE_SCHEMA,
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
