"""The nut component."""

from __future__ import annotations

from typing import Final

from homeassistant.components.sensor import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    SensorEntityDescription,
)
from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_POTENTIAL_VOLT,
    ENTITY_CATEGORY_CONFIG,
    ENTITY_CATEGORY_DIAGNOSTIC,
    FREQUENCY_HERTZ,
    PERCENTAGE,
    POWER_VOLT_AMPERE,
    POWER_WATT,
    TEMP_CELSIUS,
    TIME_SECONDS,
)

DOMAIN = "nut"

PLATFORMS = ["sensor"]

UNDO_UPDATE_LISTENER = "undo_update_listener"

DEFAULT_NAME = "NUT UPS"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3493

KEY_STATUS = "ups.status"
KEY_STATUS_DISPLAY = "ups.status.display"

COORDINATOR = "coordinator"
DEFAULT_SCAN_INTERVAL = 60

PYNUT_DATA = "data"
PYNUT_UNIQUE_ID = "unique_id"

SENSOR_TYPES: Final[dict[str, SensorEntityDescription]] = {
    "ups.status.display": SensorEntityDescription(
        key="ups.status.display",
        name="Status",
        icon="mdi:information-outline",
    ),
    "ups.status": SensorEntityDescription(
        key="ups.status",
        name="Status Data",
        icon="mdi:information-outline",
    ),
    "ups.alarm": SensorEntityDescription(
        key="ups.alarm",
        name="Alarms",
        icon="mdi:alarm",
    ),
    "ups.temperature": SensorEntityDescription(
        key="ups.temperature",
        name="UPS Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "ups.load": SensorEntityDescription(
        key="ups.load",
        name="Load",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "ups.load.high": SensorEntityDescription(
        key="ups.load.high",
        name="Overload Setting",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "ups.id": SensorEntityDescription(
        key="ups.id",
        name="System identifier",
        icon="mdi:information-outline",
    ),
    "ups.delay.start": SensorEntityDescription(
        key="ups.delay.start",
        name="Load Restart Delay",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "ups.delay.reboot": SensorEntityDescription(
        key="ups.delay.reboot",
        name="UPS Reboot Delay",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "ups.delay.shutdown": SensorEntityDescription(
        key="ups.delay.shutdown",
        name="UPS Shutdown Delay",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "ups.timer.start": SensorEntityDescription(
        key="ups.timer.start",
        name="Load Start Timer",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
    ),
    "ups.timer.reboot": SensorEntityDescription(
        key="ups.timer.reboot",
        name="Load Reboot Timer",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
    ),
    "ups.timer.shutdown": SensorEntityDescription(
        key="ups.timer.shutdown",
        name="Load Shutdown Timer",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
    ),
    "ups.test.interval": SensorEntityDescription(
        key="ups.test.interval",
        name="Self-Test Interval",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "ups.test.result": SensorEntityDescription(
        key="ups.test.result",
        name="Self-Test Result",
        icon="mdi:information-outline",
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "ups.test.date": SensorEntityDescription(
        key="ups.test.date",
        name="Self-Test Date",
        icon="mdi:calendar",
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "ups.display.language": SensorEntityDescription(
        key="ups.display.language",
        name="Language",
        icon="mdi:information-outline",
    ),
    "ups.contacts": SensorEntityDescription(
        key="ups.contacts",
        name="External Contacts",
        icon="mdi:information-outline",
    ),
    "ups.efficiency": SensorEntityDescription(
        key="ups.efficiency",
        name="Efficiency",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "ups.power": SensorEntityDescription(
        key="ups.power",
        name="Current Apparent Power",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        icon="mdi:flash",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "ups.power.nominal": SensorEntityDescription(
        key="ups.power.nominal",
        name="Nominal Power",
        native_unit_of_measurement=POWER_VOLT_AMPERE,
        icon="mdi:flash",
    ),
    "ups.realpower": SensorEntityDescription(
        key="ups.realpower",
        name="Current Real Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "ups.realpower.nominal": SensorEntityDescription(
        key="ups.realpower.nominal",
        name="Nominal Real Power",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
    ),
    "ups.beeper.status": SensorEntityDescription(
        key="ups.beeper.status",
        name="Beeper Status",
        icon="mdi:information-outline",
    ),
    "ups.type": SensorEntityDescription(
        key="ups.type",
        name="UPS Type",
        icon="mdi:information-outline",
    ),
    "ups.watchdog.status": SensorEntityDescription(
        key="ups.watchdog.status",
        name="Watchdog Status",
        icon="mdi:information-outline",
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "ups.start.auto": SensorEntityDescription(
        key="ups.start.auto",
        name="Start on AC",
        icon="mdi:information-outline",
    ),
    "ups.start.battery": SensorEntityDescription(
        key="ups.start.battery",
        name="Start on Battery",
        icon="mdi:information-outline",
    ),
    "ups.start.reboot": SensorEntityDescription(
        key="ups.start.reboot",
        name="Reboot on Battery",
        icon="mdi:information-outline",
    ),
    "ups.shutdown": SensorEntityDescription(
        key="ups.shutdown",
        name="Shutdown Ability",
        icon="mdi:information-outline",
    ),
    "battery.charge": SensorEntityDescription(
        key="battery.charge",
        name="Battery Charge",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_BATTERY,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "battery.charge.low": SensorEntityDescription(
        key="battery.charge.low",
        name="Low Battery Setpoint",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "battery.charge.restart": SensorEntityDescription(
        key="battery.charge.restart",
        name="Minimum Battery to Start",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
    ),
    "battery.charge.warning": SensorEntityDescription(
        key="battery.charge.warning",
        name="Warning Battery Setpoint",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:gauge",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "battery.charger.status": SensorEntityDescription(
        key="battery.charger.status",
        name="Charging Status",
        icon="mdi:information-outline",
    ),
    "battery.voltage": SensorEntityDescription(
        key="battery.voltage",
        name="Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "battery.voltage.nominal": SensorEntityDescription(
        key="battery.voltage.nominal",
        name="Nominal Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "battery.voltage.low": SensorEntityDescription(
        key="battery.voltage.low",
        name="Low Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "battery.voltage.high": SensorEntityDescription(
        key="battery.voltage.high",
        name="High Battery Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "battery.capacity": SensorEntityDescription(
        key="battery.capacity",
        name="Battery Capacity",
        native_unit_of_measurement="Ah",
        icon="mdi:flash",
    ),
    "battery.current": SensorEntityDescription(
        key="battery.current",
        name="Battery Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        icon="mdi:flash",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "battery.current.total": SensorEntityDescription(
        key="battery.current.total",
        name="Total Battery Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        icon="mdi:flash",
    ),
    "battery.temperature": SensorEntityDescription(
        key="battery.temperature",
        name="Battery Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "battery.runtime": SensorEntityDescription(
        key="battery.runtime",
        name="Battery Runtime",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    "battery.runtime.low": SensorEntityDescription(
        key="battery.runtime.low",
        name="Low Battery Runtime",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
    ),
    "battery.runtime.restart": SensorEntityDescription(
        key="battery.runtime.restart",
        name="Minimum Battery Runtime to Start",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:timer-outline",
    ),
    "battery.alarm.threshold": SensorEntityDescription(
        key="battery.alarm.threshold",
        name="Battery Alarm Threshold",
        icon="mdi:information-outline",
        entity_category=ENTITY_CATEGORY_CONFIG,
    ),
    "battery.date": SensorEntityDescription(
        key="battery.date",
        name="Battery Date",
        icon="mdi:calendar",
    ),
    "battery.mfr.date": SensorEntityDescription(
        key="battery.mfr.date",
        name="Battery Manuf. Date",
        icon="mdi:calendar",
    ),
    "battery.packs": SensorEntityDescription(
        key="battery.packs",
        name="Number of Batteries",
        icon="mdi:information-outline",
    ),
    "battery.packs.bad": SensorEntityDescription(
        key="battery.packs.bad",
        name="Number of Bad Batteries",
        icon="mdi:information-outline",
    ),
    "battery.type": SensorEntityDescription(
        key="battery.type",
        name="Battery Chemistry",
        icon="mdi:information-outline",
    ),
    "input.sensitivity": SensorEntityDescription(
        key="input.sensitivity",
        name="Input Power Sensitivity",
        icon="mdi:information-outline",
    ),
    "input.transfer.low": SensorEntityDescription(
        key="input.transfer.low",
        name="Low Voltage Transfer",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "input.transfer.high": SensorEntityDescription(
        key="input.transfer.high",
        name="High Voltage Transfer",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "input.transfer.reason": SensorEntityDescription(
        key="input.transfer.reason",
        name="Voltage Transfer Reason",
        icon="mdi:information-outline",
    ),
    "input.voltage": SensorEntityDescription(
        key="input.voltage",
        name="Input Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "input.voltage.nominal": SensorEntityDescription(
        key="input.voltage.nominal",
        name="Nominal Input Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "input.frequency": SensorEntityDescription(
        key="input.frequency",
        name="Input Line Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        icon="mdi:flash",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "input.frequency.nominal": SensorEntityDescription(
        key="input.frequency.nominal",
        name="Nominal Input Line Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        icon="mdi:flash",
    ),
    "input.frequency.status": SensorEntityDescription(
        key="input.frequency.status",
        name="Input Frequency Status",
        icon="mdi:information-outline",
    ),
    "output.current": SensorEntityDescription(
        key="output.current",
        name="Output Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        icon="mdi:flash",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "output.current.nominal": SensorEntityDescription(
        key="output.current.nominal",
        name="Nominal Output Current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        icon="mdi:flash",
    ),
    "output.voltage": SensorEntityDescription(
        key="output.voltage",
        name="Output Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "output.voltage.nominal": SensorEntityDescription(
        key="output.voltage.nominal",
        name="Nominal Output Voltage",
        native_unit_of_measurement=ELECTRIC_POTENTIAL_VOLT,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    "output.frequency": SensorEntityDescription(
        key="output.frequency",
        name="Output Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        icon="mdi:flash",
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "output.frequency.nominal": SensorEntityDescription(
        key="output.frequency.nominal",
        name="Nominal Output Frequency",
        native_unit_of_measurement=FREQUENCY_HERTZ,
        icon="mdi:flash",
    ),
    "ambient.humidity": SensorEntityDescription(
        key="ambient.humidity",
        name="Ambient Humidity",
        native_unit_of_measurement=PERCENTAGE,
        device_class=DEVICE_CLASS_HUMIDITY,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "ambient.temperature": SensorEntityDescription(
        key="ambient.temperature",
        name="Ambient Temperature",
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "watts": SensorEntityDescription(
        key="watts",
        name="Watts",
        native_unit_of_measurement=POWER_WATT,
        device_class=DEVICE_CLASS_POWER,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}

STATE_TYPES = {
    "OL": "Online",
    "OB": "On Battery",
    "LB": "Low Battery",
    "HB": "High Battery",
    "RB": "Battery Needs Replaced",
    "CHRG": "Battery Charging",
    "DISCHRG": "Battery Discharging",
    "BYPASS": "Bypass Active",
    "CAL": "Runtime Calibration",
    "OFF": "Offline",
    "OVER": "Overloaded",
    "TRIM": "Trimming Voltage",
    "BOOST": "Boosting Voltage",
    "FSD": "Forced Shutdown",
    "ALARM": "Alarm",
}
