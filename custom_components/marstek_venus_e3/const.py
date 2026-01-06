"""Constants for the Marstek Venus E 3.0 integration."""

DOMAIN = "marstek_venus_e3"

# Configuration
CONF_IP_ADDRESS = "ip_address"
CONF_PORT = "port"
DEFAULT_PORT = 30000
DEFAULT_SCAN_INTERVAL = 60
DEFAULT_TIMEOUT = 2.0
DEFAULT_MAX_RETRIES = 3

# UDP Commands
CMD_GET_MODE = "ES.GetMode"
CMD_GET_BAT_STATUS = "Bat.GetStatus"
CMD_SET_MODE = "ES.SetMode"

# Sensor keys
SENSOR_SOC = "soc"
SENSOR_BAT_TEMP = "bat_temp"
SENSOR_BAT_VOLTAGE = "bat_voltage"
SENSOR_BAT_CURRENT = "bat_current"
SENSOR_BAT_POWER = "bat_power"
SENSOR_ONGRID_POWER = "ongrid_power"
SENSOR_LOAD_POWER = "load_power"
SENSOR_PV_POWER = "pv_power"
SENSOR_ES_MODE = "es_mode"
SENSOR_CHARGE_POWER = "charge_power"
SENSOR_DISCHARGE_POWER = "discharge_power"

# ES Modes
ES_MODES = {
    0: "Auto",
    1: "AI",
    2: "Manual",
    3: "Passive"
}
