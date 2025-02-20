"""Support for the sensors in a GreenEye Monitor."""
from __future__ import annotations

from typing import Any, Generic, TypeVar

import greeneye
from greeneye import Monitors

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_SENSOR_TYPE,
    CONF_SENSORS,
    CONF_TEMPERATURE_UNIT,
    DEVICE_CLASS_TEMPERATURE,
    ELECTRIC_POTENTIAL_VOLT,
    POWER_WATT,
    TIME_HOURS,
    TIME_MINUTES,
    TIME_SECONDS,
)
from homeassistant.core import Config, HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import DiscoveryInfoType

from . import (
    CONF_COUNTED_QUANTITY,
    CONF_COUNTED_QUANTITY_PER_PULSE,
    CONF_MONITOR_SERIAL_NUMBER,
    CONF_NET_METERING,
    CONF_NUMBER,
    CONF_TIME_UNIT,
    DATA_GREENEYE_MONITOR,
    SENSOR_TYPE_CURRENT,
    SENSOR_TYPE_PULSE_COUNTER,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_VOLTAGE,
)

DATA_PULSES = "pulses"
DATA_WATT_SECONDS = "watt_seconds"

UNIT_WATTS = POWER_WATT

COUNTER_ICON = "mdi:counter"
CURRENT_SENSOR_ICON = "mdi:flash"
TEMPERATURE_ICON = "mdi:thermometer"
VOLTAGE_ICON = "mdi:current-ac"


async def async_setup_platform(
    hass: HomeAssistant,
    config: Config,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType,
) -> None:
    """Set up a single GEM temperature sensor."""
    entities: list[GEMSensor] = []
    for sensor in discovery_info[CONF_SENSORS]:
        sensor_type = sensor[CONF_SENSOR_TYPE]
        if sensor_type == SENSOR_TYPE_CURRENT:
            entities.append(
                CurrentSensor(
                    sensor[CONF_MONITOR_SERIAL_NUMBER],
                    sensor[CONF_NUMBER],
                    sensor[CONF_NAME],
                    sensor[CONF_NET_METERING],
                )
            )
        elif sensor_type == SENSOR_TYPE_PULSE_COUNTER:
            entities.append(
                PulseCounter(
                    sensor[CONF_MONITOR_SERIAL_NUMBER],
                    sensor[CONF_NUMBER],
                    sensor[CONF_NAME],
                    sensor[CONF_COUNTED_QUANTITY],
                    sensor[CONF_TIME_UNIT],
                    sensor[CONF_COUNTED_QUANTITY_PER_PULSE],
                )
            )
        elif sensor_type == SENSOR_TYPE_TEMPERATURE:
            entities.append(
                TemperatureSensor(
                    sensor[CONF_MONITOR_SERIAL_NUMBER],
                    sensor[CONF_NUMBER],
                    sensor[CONF_NAME],
                    sensor[CONF_TEMPERATURE_UNIT],
                )
            )
        elif sensor_type == SENSOR_TYPE_VOLTAGE:
            entities.append(
                VoltageSensor(
                    sensor[CONF_MONITOR_SERIAL_NUMBER],
                    sensor[CONF_NUMBER],
                    sensor[CONF_NAME],
                )
            )

    async_add_entities(entities)


T = TypeVar(
    "T",
    greeneye.monitor.Channel,
    greeneye.monitor.Monitor,
    greeneye.monitor.PulseCounter,
    greeneye.monitor.TemperatureSensor,
)


class GEMSensor(Generic[T], SensorEntity):
    """Base class for GreenEye Monitor sensors."""

    _attr_should_poll = False

    def __init__(
        self, monitor_serial_number: int, name: str, sensor_type: str, number: int
    ) -> None:
        """Construct the entity."""
        self._monitor_serial_number = monitor_serial_number
        self._name = name
        self._sensor: T | None = None
        self._sensor_type = sensor_type
        self._number = number

    @property
    def unique_id(self) -> str:
        """Return a unique ID for this sensor."""
        return f"{self._monitor_serial_number}-{self._sensor_type}-{self._number}"

    @property
    def name(self) -> str:
        """Return the name of the channel."""
        return self._name

    async def async_added_to_hass(self) -> None:
        """Wait for and connect to the sensor."""
        monitors = self.hass.data[DATA_GREENEYE_MONITOR]

        if not self._try_connect_to_monitor(monitors):
            monitors.add_listener(self._on_new_monitor)

    def _on_new_monitor(self, *args: list[Any]) -> None:
        monitors = self.hass.data[DATA_GREENEYE_MONITOR]
        if self._try_connect_to_monitor(monitors):
            monitors.remove_listener(self._on_new_monitor)

    async def async_will_remove_from_hass(self) -> None:
        """Remove listener from the sensor."""
        if self._sensor:
            self._sensor.remove_listener(self.async_write_ha_state)
        else:
            monitors = self.hass.data[DATA_GREENEYE_MONITOR]
            monitors.remove_listener(self._on_new_monitor)

    def _try_connect_to_monitor(self, monitors: Monitors) -> bool:
        monitor = monitors.monitors.get(self._monitor_serial_number)
        if not monitor:
            return False

        self._sensor = self._get_sensor(monitor)
        self._sensor.add_listener(self.async_write_ha_state)
        self.async_write_ha_state()

        return True

    def _get_sensor(self, monitor: greeneye.monitor.Monitor) -> T:
        raise NotImplementedError()


class CurrentSensor(GEMSensor[greeneye.monitor.Channel]):
    """Entity showing power usage on one channel of the monitor."""

    _attr_icon = CURRENT_SENSOR_ICON
    _attr_native_unit_of_measurement = UNIT_WATTS

    def __init__(
        self, monitor_serial_number: int, number: int, name: str, net_metering: bool
    ) -> None:
        """Construct the entity."""
        super().__init__(monitor_serial_number, name, "current", number)
        self._net_metering = net_metering

    def _get_sensor(
        self, monitor: greeneye.monitor.Monitor
    ) -> greeneye.monitor.Channel:
        return monitor.channels[self._number - 1]

    @property
    def native_value(self) -> float | None:
        """Return the current number of watts being used by the channel."""
        if not self._sensor:
            return None

        assert isinstance(self._sensor.watts, float)
        return self._sensor.watts

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return total wattseconds in the state dictionary."""
        if not self._sensor:
            return None

        if self._net_metering:
            watt_seconds = self._sensor.polarized_watt_seconds
        else:
            watt_seconds = self._sensor.absolute_watt_seconds

        return {DATA_WATT_SECONDS: watt_seconds}


class PulseCounter(GEMSensor[greeneye.monitor.PulseCounter]):
    """Entity showing rate of change in one pulse counter of the monitor."""

    _attr_icon = COUNTER_ICON

    def __init__(
        self,
        monitor_serial_number: int,
        number: int,
        name: str,
        counted_quantity: str,
        time_unit: str,
        counted_quantity_per_pulse: float,
    ) -> None:
        """Construct the entity."""
        super().__init__(monitor_serial_number, name, "pulse", number)
        self._counted_quantity = counted_quantity
        self._counted_quantity_per_pulse = counted_quantity_per_pulse
        self._time_unit = time_unit

    def _get_sensor(
        self, monitor: greeneye.monitor.Monitor
    ) -> greeneye.monitor.PulseCounter:
        return monitor.pulse_counters[self._number - 1]

    @property
    def native_value(self) -> float | None:
        """Return the current rate of change for the given pulse counter."""
        if not self._sensor or self._sensor.pulses_per_second is None:
            return None

        result = (
            self._sensor.pulses_per_second
            * self._counted_quantity_per_pulse
            * self._seconds_per_time_unit
        )
        assert isinstance(result, float)
        return result

    @property
    def _seconds_per_time_unit(self) -> int:
        """Return the number of seconds in the given display time unit."""
        if self._time_unit == TIME_SECONDS:
            return 1
        if self._time_unit == TIME_MINUTES:
            return 60
        if self._time_unit == TIME_HOURS:
            return 3600

        # Config schema should have ensured it is one of the above values
        raise Exception(
            f"Invalid value for time unit: {self._time_unit}. Expected one of {TIME_SECONDS}, {TIME_MINUTES}, or {TIME_HOURS}"
        )

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement for this pulse counter."""
        return f"{self._counted_quantity}/{self._time_unit}"

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return total pulses in the data dictionary."""
        if not self._sensor:
            return None

        return {DATA_PULSES: self._sensor.pulses}


class TemperatureSensor(GEMSensor[greeneye.monitor.TemperatureSensor]):
    """Entity showing temperature from one temperature sensor."""

    _attr_device_class = DEVICE_CLASS_TEMPERATURE
    _attr_icon = TEMPERATURE_ICON

    def __init__(
        self, monitor_serial_number: int, number: int, name: str, unit: str
    ) -> None:
        """Construct the entity."""
        super().__init__(monitor_serial_number, name, "temp", number)
        self._unit = unit

    def _get_sensor(
        self, monitor: greeneye.monitor.Monitor
    ) -> greeneye.monitor.TemperatureSensor:
        return monitor.temperature_sensors[self._number - 1]

    @property
    def native_value(self) -> float | None:
        """Return the current temperature being reported by this sensor."""
        if not self._sensor:
            return None

        assert isinstance(self._sensor.temperature, float)
        return self._sensor.temperature

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement for this sensor (user specified)."""
        return self._unit


class VoltageSensor(GEMSensor[greeneye.monitor.Monitor]):
    """Entity showing voltage."""

    _attr_icon = VOLTAGE_ICON
    _attr_native_unit_of_measurement = ELECTRIC_POTENTIAL_VOLT

    def __init__(self, monitor_serial_number: int, number: int, name: str) -> None:
        """Construct the entity."""
        super().__init__(monitor_serial_number, name, "volts", number)

    def _get_sensor(
        self, monitor: greeneye.monitor.Monitor
    ) -> greeneye.monitor.Monitor:
        """Wire the updates to the monitor itself, since there is no voltage element in the API."""
        return monitor

    @property
    def native_value(self) -> float | None:
        """Return the current voltage being reported by this sensor."""
        if not self._sensor:
            return None

        assert isinstance(self._sensor.voltage, float)
        return self._sensor.voltage
