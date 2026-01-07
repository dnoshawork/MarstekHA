"""Data coordinator for Marstek Venus E 3.0."""
import asyncio
import json
import logging
import socket
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES,
    CMD_GET_MODE,
)

_LOGGER = logging.getLogger(__name__)


class MarstekVenusE3Coordinator(DataUpdateCoordinator):
    """Class to manage fetching Marstek Venus E 3.0 data."""

    def __init__(
        self,
        hass: HomeAssistant,
        ip_address: str,
        port: int = DEFAULT_PORT,
        scan_interval: int = 30,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.ip_address = ip_address
        self.port = port
        self.timeout = DEFAULT_TIMEOUT
        self.max_retries = DEFAULT_MAX_RETRIES

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the battery."""
        try:
            # Get ES Mode data (contains all necessary information)
            es_mode_data = await self._execute_command_with_retry(CMD_GET_MODE)

            # Parse the data
            data = self._parse_data(es_mode_data)

            return data

        except Exception as err:
            raise UpdateFailed(f"Error communicating with device: {err}") from err

    async def _execute_command_with_retry(
        self,
        command: str,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """Execute a command with retry mechanism (inspired by Jeedom script)."""
        if params is None:
            params = {"id": 0}

        request = {
            "id": 1,
            "method": command,
            "params": params,
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                # Progressive timeout: base + (attempt - 1) seconds
                timeout = self.timeout + (attempt - 1)

                _LOGGER.debug(
                    "Sending command %s (attempt %d/%d, timeout=%ds)",
                    command,
                    attempt,
                    self.max_retries,
                    timeout,
                )

                response = await self._send_udp_command(request, timeout)

                # Check for parse errors that require retry
                if isinstance(response, dict) and response.get("error"):
                    error_code = response["error"].get("code", 0)
                    if error_code == -32700:  # Parse error
                        _LOGGER.warning(
                            "Parse error on attempt %d/%d, retrying...",
                            attempt,
                            self.max_retries,
                        )
                        if attempt < self.max_retries:
                            # Exponential backoff: 2^attempt seconds
                            await asyncio.sleep(2 ** attempt)
                            continue

                # Valid response with result
                if isinstance(response, dict) and "result" in response:
                    _LOGGER.debug("Command %s successful on attempt %d", command, attempt)
                    return response

                # If we're here, response is invalid but not a parse error
                if attempt < self.max_retries:
                    _LOGGER.warning(
                        "Invalid response on attempt %d/%d, retrying...",
                        attempt,
                        self.max_retries,
                    )
                    await asyncio.sleep(2 ** attempt)
                    continue

            except (socket.timeout, asyncio.TimeoutError) as err:
                _LOGGER.warning(
                    "Timeout on attempt %d/%d: %s",
                    attempt,
                    self.max_retries,
                    err,
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise UpdateFailed(f"Command {command} failed after {self.max_retries} attempts") from err

            except Exception as err:
                _LOGGER.error("Unexpected error on attempt %d/%d: %s", attempt, self.max_retries, err)
                if attempt < self.max_retries:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise UpdateFailed(f"Command {command} failed: {err}") from err

        raise UpdateFailed(f"Command {command} failed after {self.max_retries} attempts")

    async def _send_udp_command(
        self,
        request: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        """Send UDP command and get response."""
        loop = asyncio.get_event_loop()

        def _send_and_receive():
            """Send and receive UDP data (blocking operation)."""
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Bind to an ephemeral port (0 = let OS choose a free port)
                # This avoids conflicts if port 30000 is already in use locally
                sock.bind(("0.0.0.0", 0))
                sock.settimeout(timeout)

                # Get the actual port assigned by the OS
                local_port = sock.getsockname()[1]
                _LOGGER.debug("Bound to local port %d for receiving responses", local_port)

                # Send request (use separators for compact JSON like Jeedom script)
                message = json.dumps(request, separators=(",", ":")).encode("utf-8")
                _LOGGER.debug("Sending UDP request to %s:%d: %s", self.ip_address, self.port, message.decode("utf-8"))
                sock.sendto(message, (self.ip_address, self.port))

                # Receive response with better error handling
                try:
                    data, addr = sock.recvfrom(65535)
                    _LOGGER.debug("Received UDP response from %s: %s", addr, data.decode("utf-8"))
                    response = json.loads(data.decode("utf-8", errors="strict"))
                    return response
                except socket.timeout as err:
                    _LOGGER.error("UDP socket timeout while waiting for response from %s:%d", self.ip_address, self.port)
                    raise
                except json.JSONDecodeError as err:
                    _LOGGER.error("Failed to decode JSON response: %s", err)
                    raise
                except Exception as err:
                    _LOGGER.error("Error receiving UDP response: %s", err)
                    raise

            except OSError as err:
                _LOGGER.error("UDP socket error (port %d may be in use): %s", self.port, err)
                raise
            finally:
                sock.close()

        # Run blocking operation in executor
        return await loop.run_in_executor(None, _send_and_receive)

    def _parse_data(
        self,
        es_mode_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Parse the response data into sensor values.

        The battery returns all data in ES.GetMode response with this format:
        {
            "id": 1,
            "src": "VenusE 3.0-009b08a5e322",
            "result": {
                "id": 0,
                "mode": "Auto",  # String: "Auto", "AI", "Manual", "Passive"
                "ongrid_power": 437,
                "offgrid_power": 0,
                "bat_soc": 81,  # State of Charge in %
                "ct_state": 0,
                "a_power": 0,
                "b_power": 0,
                "c_power": 0,
                "total_power": 0,
                "input_energy": 0,
                "output_energy": 0
            }
        }
        """
        data = {}

        if "result" in es_mode_data:
            result = es_mode_data["result"]

            # Mode (string format: "Auto", "AI", "Manual", "Passive")
            mode_str = result.get("mode", "Unknown")
            data["es_mode"] = mode_str

            # Battery data
            data["soc"] = result.get("bat_soc", 0)

            # Power data
            data["ongrid_power"] = result.get("ongrid_power", 0)
            data["offgrid_power"] = result.get("offgrid_power", 0)

            # Phase powers
            data["a_power"] = result.get("a_power", 0)
            data["b_power"] = result.get("b_power", 0)
            data["c_power"] = result.get("c_power", 0)
            data["total_power"] = result.get("total_power", 0)

            # Energy counters
            data["input_energy"] = result.get("input_energy", 0)
            data["output_energy"] = result.get("output_energy", 0)

        return data

    async def async_set_mode(
        self,
        mode: int,
        start_time: str | None = None,
        end_time: str | None = None,
        week_set: int = 127,
        power: int = 0,
        enable: int = 1,
        time_num: int = 1,
        cd_time: int | None = None,
    ) -> bool:
        """Set the ES mode of the battery.

        Args:
            mode: Operating mode (0=Auto, 1=AI, 2=Manual, 3=Passive)
            start_time: Start time for Manual mode (format "HH:MM")
            end_time: End time for Manual mode (format "HH:MM")
            week_set: Days of week bitmap for Manual mode (0-127, default 127=all days)
                      bit 0=Monday, bit 1=Tuesday, ..., bit 6=Sunday
            power: Power in watts for Manual mode (negative=charge, positive=discharge)
                   or power limit for Passive mode
            enable: Enable flag for Manual mode (0=disabled, 1=enabled)
            time_num: Time period serial number (0-9) for Manual mode
            cd_time: Duration in seconds for Passive mode (cmd_time)
        """
        try:
            # For Manual mode (mode=2), we need to send manual_cfg
            if mode == 2:
                if start_time is None or end_time is None:
                    _LOGGER.error("Manual mode requires start_time and end_time")
                    return False

                params = {
                    "id": 0,
                    "config": {
                        "mode": "Manual",
                        "manual_cfg": {
                            "time_num": time_num,
                            "start_time": start_time,
                            "end_time": end_time,
                            "week_set": week_set,
                            "power": power,
                            "enable": enable,
                        }
                    }
                }
            elif mode == 3:  # Passive mode
                # For Passive mode, we need to send passive_cfg with power and cd_time
                params = {
                    "id": 0,
                    "config": {
                        "mode": "Passive",
                        "passive_cfg": {
                            "power": power,
                            "cd_time": cd_time if cd_time is not None else 300,  # Default 300 seconds
                        }
                    }
                }
            else:
                # For Auto and AI modes, just send the mode
                params = {
                    "id": 0,
                    "mode": mode,
                }

            response = await self._execute_command_with_retry(
                "ES.SetMode",
                params=params,
            )

            return "result" in response and response["result"].get("success", False)

        except Exception as err:
            _LOGGER.error("Failed to set mode: %s", err)
            return False
