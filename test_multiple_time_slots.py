#!/usr/bin/env python3
"""
Test script to demonstrate multiple time slot configuration for Marstek Venus E 3.0.

This script shows how to use the new time_num parameter to configure multiple
time slots in Manual mode.
"""

def test_multiple_time_slots():
    """Test configuration for multiple time slots."""

    # Example 1: Configure time slot 0 (morning charge)
    print("Configuring time slot 0 - Morning charge:")
    print("service: marstek_venus_e3.set_mode")
    print("data:")
    print("  device_id: YOUR_DEVICE_ID")
    print("  mode: \"2\"  # Manual mode")
    print("  time_num: 0  # First time slot")
    print("  start_time: \"08:00\"")
    print("  end_time: \"12:00\"")
    print("  days: [\"monday\", \"tuesday\", \"wednesday\", \"thursday\", \"friday\"]")
    print("  power: -1000  # Charge at 1000W (negative)")
    print("  enable: 1")
    print()

    # Example 2: Configure time slot 1 (evening discharge)
    print("Configuring time slot 1 - Evening discharge:")
    print("service: marstek_venus_e3.set_mode")
    print("data:")
    print("  device_id: YOUR_DEVICE_ID")
    print("  mode: \"2\"  # Manual mode")
    print("  time_num: 1  # Second time slot")
    print("  start_time: \"17:00\"")
    print("  end_time: \"22:00\"")
    print("  days: [\"monday\", \"tuesday\", \"wednesday\", \"thursday\", \"friday\"]")
    print("  power: 2000  # Discharge at 2000W (positive)")
    print("  enable: 1")
    print()

    # Example 3: Configure time slot 2 (weekend charging)
    print("Configuring time slot 2 - Weekend charging:")
    print("service: marstek_venus_e3.set_mode")
    print("data:")
    print("  device_id: YOUR_DEVICE_ID")
    print("  mode: \"2\"  # Manual mode")
    print("  time_num: 2  # Third time slot")
    print("  start_time: \"09:00\"")
    print("  end_time: \"18:00\"")
    print("  days: [\"saturday\", \"sunday\"]")
    print("  power: -1500  # Charge at 1500W (negative)")
    print("  enable: 1")
    print()

    # Example 4: Disable a time slot
    print("Disabling time slot 0:")
    print("service: marstek_venus_e3.set_mode")
    print("data:")
    print("  device_id: YOUR_DEVICE_ID")
    print("  mode: \"2\"  # Manual mode")
    print("  time_num: 0  # First time slot")
    print("  enable: 0  # Disable this time slot")
    print()

    print("Key points:")
    print("- time_num can be 0-9 (10 different time slots)")
    print("- Each time slot can have different start/end times, days, power, and enable status")
    print("- To configure multiple time slots, call the service multiple times with different time_num values")
    print("- The device supports up to 10 time slots simultaneously")
    print("- Use enable: 0 to disable a specific time slot without deleting its configuration")

if __name__ == "__main__":
    test_multiple_time_slots()
