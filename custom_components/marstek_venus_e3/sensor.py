"""Sensor platform for Marstek Venus E 3.0."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_IP_ADDRESS
from .coordinator import MarstekVenusE3Coordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class MarstekSensorEntityDescription(SensorEntityDescription):
    """Describes Marstek sensor entity."""

    value_fn: Callable[[dict], float | int | str | None] = None


SENSOR_TYPES: tuple[MarstekSensorEntityDescription, ...] = (
    MarstekSensorEntityDescription(
        key="soc",
        name="State of Charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("soc"),
    ),
    MarstekSensorEntityDescription(
        key="es_mode",
        name="ES Mode",
        device_class=SensorDeviceClass.ENUM,
        value_fn=lambda data: data.get("es_mode"),
    ),
    MarstekSensorEntityDescription(
        key="ongrid_power",
        name="Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("ongrid_power"),
    ),
    MarstekSensorEntityDescription(
        key="offgrid_power",
        name="Off-Grid Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("offgrid_power"),
    ),
    MarstekSensorEntityDescription(
        key="a_power",
        name="Phase A Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("a_power"),
    ),
    MarstekSensorEntityDescription(
        key="b_power",
        name="Phase B Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("b_power"),
    ),
    MarstekSensorEntityDescription(
        key="c_power",
        name="Phase C Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("c_power"),
    ),
    MarstekSensorEntityDescription(
        key="total_power",
        name="Total Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.get("total_power"),
    ),
    MarstekSensorEntityDescription(
        key="input_energy",
        name="Input Energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.get("input_energy"),
    ),
    MarstekSensorEntityDescription(
        key="output_energy",
        name="Output Energy",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.get("output_energy"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Marstek Venus E 3.0 sensors based on a config entry."""
    coordinator: MarstekVenusE3Coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        MarstekSensor(coordinator, entry, description)
        for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class MarstekSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Marstek Venus E 3.0 sensor."""

    entity_description: MarstekSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: MarstekVenusE3Coordinator,
        entry: ConfigEntry,
        description: MarstekSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"Marstek Venus E 3.0 ({entry.data[CONF_IP_ADDRESS]})",
            manufacturer="Marstek",
            model="Venus E 3.0",
        )

    @property
    def native_value(self) -> float | int | str | None:
        """Return the state of the sensor."""
        if self.coordinator.data and self.entity_description.value_fn:
            return self.entity_description.value_fn(self.coordinator.data)
        return None
