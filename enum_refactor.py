#!/bin/python

import glob
import re
import isort
import sys

subs = [
    # sensor state class
    (
        "STATE_CLASS_MEASUREMENT",
        "SensorStateClass",
        "MEASUREMENT",
        "homeassistant.components.sensor",
    ),
    (
        "STATE_CLASS_TOTAL",
        "SensorStateClass",
        "TOTAL",
        "homeassistant.components.sensor",
    ),
    (
        "STATE_CLASS_TOTAL_INCREASING",
        "SensorStateClass",
        "TOTAL_INCREASING",
        "homeassistant.components.sensor",
    ),

    # entity category
    (
        "ENTITY_CATEGORY_CONFIG",
        "EntityCategory",
        "CONFIG",
        "homeassistant.helpers.entity",
    ),
    (
        "ENTITY_CATEGORY_DIAGNOSTIC",
        "EntityCategory",
        "DIAGNOSTIC",
        "homeassistant.helpers.entity",
    ),
    (
        "ENTITY_CATEGORY_SYSTEM",
        "EntityCategory",
        "SYSTEM",
        "homeassistant.helpers.entity",
    ),

    # sensor device class
    (
        "DEVICE_CLASS_AQI",
        "SensorDeviceClass",
        "AQI",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_BATTERY",
        "SensorDeviceClass",
        "BATTERY",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_CO",
        "SensorDeviceClass",
        "CO",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_CO2",
        "SensorDeviceClass",
        "CO2",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_CURRENT",
        "SensorDeviceClass",
        "CURRENT",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_DATE",
        "SensorDeviceClass",
        "DATE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_ENERGY",
        "SensorDeviceClass",
        "ENERGY",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_FREQUENCY",
        "SensorDeviceClass",
        "FREQUENCY",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_GAS",
        "SensorDeviceClass",
        "GAS",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_HUMIDITY",
        "SensorDeviceClass",
        "HUMIDITY",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_ILLUMINANCE",
        "SensorDeviceClass",
        "ILLUMINANCE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_MONETARY",
        "SensorDeviceClass",
        "MONETARY",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_NITROGEN_DIOXIDE",
        "SensorDeviceClass",
        "NITROGEN_DIOXIDE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_NITROGEN_MONOXIDE",
        "SensorDeviceClass",
        "NITROGEN_MONOXIDE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_NITROUS_OXIDE",
        "SensorDeviceClass",
        "NITROUS_OXIDE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_OZONE",
        "SensorDeviceClass",
        "OZONE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_PM1",
        "SensorDeviceClass",
        "PM1",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_PM10",
        "SensorDeviceClass",
        "PM10",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_PM25",
        "SensorDeviceClass",
        "PM25",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_POWER_FACTOR",
        "SensorDeviceClass",
        "POWER_FACTOR",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_POWER",
        "SensorDeviceClass",
        "POWER",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_PRESSURE",
        "SensorDeviceClass",
        "PRESSURE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_SIGNAL_STRENGTH",
        "SensorDeviceClass",
        "SIGNAL_STRENGTH",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_SULPHUR_DIOXIDE",
        "SensorDeviceClass",
        "SULPHUR_DIOXIDE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_TEMPERATURE",
        "SensorDeviceClass",
        "TEMPERATURE",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_TIMESTAMP",
        "SensorDeviceClass",
        "TIMESTAMP",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_VOLATILE_ORGANIC_COMPOUNDS",
        "SensorDeviceClass",
        "VOLATILE_ORGANIC_COMPOUNDS",
        "homeassistant.components.sensor",
    ),
    (
        "DEVICE_CLASS_VOLTAGE",
        "SensorDeviceClass",
        "VOLTAGE",
        "homeassistant.components.sensor",
    ),

    # Binary sensor device class
    (
        "DEVICE_CLASS_BATTERY",
        "BinarySensorDeviceClass",
        "BATTERY",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_BATTERY_CHARGING",
        "BinarySensorDeviceClass",
        "BATTERY_CHARGING",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_COLD",
        "BinarySensorDeviceClass",
        "COLD",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_CONNECTIVITY",
        "BinarySensorDeviceClass",
        "CONNECTIVITY",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_DOOR",
        "BinarySensorDeviceClass",
        "DOOR",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_GARAGE_DOOR",
        "BinarySensorDeviceClass",
        "GARAGE_DOOR",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_GAS",
        "BinarySensorDeviceClass",
        "GAS",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_HEAT",
        "BinarySensorDeviceClass",
        "HEAT",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_LIGHT",
        "BinarySensorDeviceClass",
        "LIGHT",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_LOCK",
        "BinarySensorDeviceClass",
        "LOCK",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_MOISTURE",
        "BinarySensorDeviceClass",
        "MOISTURE",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_MOTION",
        "BinarySensorDeviceClass",
        "MOTION",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_MOVING",
        "BinarySensorDeviceClass",
        "MOVING",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_OCCUPANCY",
        "BinarySensorDeviceClass",
        "OCCUPANCY",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_OPENING",
        "BinarySensorDeviceClass",
        "OPENING",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_PLUG",
        "BinarySensorDeviceClass",
        "PLUG",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_POWER",
        "BinarySensorDeviceClass",
        "POWER",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_PRESENCE",
        "BinarySensorDeviceClass",
        "PRESENCE",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_PROBLEM",
        "BinarySensorDeviceClass",
        "PROBLEM",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_RUNNING",
        "BinarySensorDeviceClass",
        "RUNNING",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_SAFETY",
        "BinarySensorDeviceClass",
        "SAFETY",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_SMOKE",
        "BinarySensorDeviceClass",
        "SMOKE",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_SOUND",
        "BinarySensorDeviceClass",
        "SOUND",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_TAMPER",
        "BinarySensorDeviceClass",
        "TAMPER",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_UPDATE",
        "BinarySensorDeviceClass",
        "UPDATE",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_VIBRATION",
        "BinarySensorDeviceClass",
        "VIBRATION",
        "homeassistant.components.binary_sensor",
    ),
    (
        "DEVICE_CLASS_WINDOW",
        "BinarySensorDeviceClass",
        "WINDOW",
        "homeassistant.components.binary_sensor",
    ),

    # Cover device class
    (
        "DEVICE_CLASS_AWNING",
        "CoverDeviceClass",
        "AWNING",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_BLIND",
        "CoverDeviceClass",
        "BLIND",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_CURTAIN",
        "CoverDeviceClass",
        "CURTAIN",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_DAMPER",
        "CoverDeviceClass",
        "DAMPER",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_DOOR",
        "CoverDeviceClass",
        "DOOR",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_GARAGE",
        "CoverDeviceClass",
        "GARAGE",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_GATE",
        "CoverDeviceClass",
        "GATE",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_SHADE",
        "CoverDeviceClass",
        "SHADE",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_SHUTTER",
        "CoverDeviceClass",
        "SHUTTER",
        "homeassistant.components.cover",
    ),
    (
        "DEVICE_CLASS_WINDOW",
        "CoverDeviceClass",
        "WINDOW",
        "homeassistant.components.cover",
    ),


    # Humidifier device classes old style are not used anywhere (skipping)
    # media player device classes
    (
        "DEVICE_CLASS_TV",
        "MediaPlayerDeviceClass",
        "TV",
        "homeassistant.components.media_player",
    ),
    (
        "DEVICE_CLASS_SPEAKER",
        "MediaPlayerDeviceClass",
        "SPEAKER",
        "homeassistant.components.media_player",
    ),
    (
        "DEVICE_CLASS_RECEIVER",
        "MediaPlayerDeviceClass",
        "RECEIVER",
        "homeassistant.components.media_player",
    ),

    # switch device classes
    (
        "DEVICE_CLASS_OUTLET",
        "SwitchDeviceClass",
        "OUTLET",
        "homeassistant.components.switch",
    ),
    (
        "DEVICE_CLASS_SWITCH",
        "SwitchDeviceClass",
        "SWITCH",
        "homeassistant.components.switch",
    ),

    # config source enums
    (
        "SOURCE_DISCOVERED",
        "ConfigSource",
        "DISCOVERED",
        "homeassistant.core",
    ),
    (
        "SOURCE_STORAGE",
        "ConfigSource",
        "STORAGE",
        "homeassistant.core",
    ),
    (
        "SOURCE_YAML",
        "ConfigSource",
        "YAML",
        "homeassistant.core",
    ),
]
# List of items that match more than one - need to manually do them!
manualsubs = []

matchers = [i[0] for i in subs]
for item in subs:
    count = matchers.count(item[0])
    if count > 1:
        #print(f"Duplicate entry {item[0]} in subs list")
        manualsubs.append(item)
        subs.remove(item)

assert len(sys.argv) == 2, "You must specify exactly one command line argument"
filesearch = sys.argv[1]
print(f" Refactoring {filesearch}")

files = glob.glob(f"tests/components/{filesearch}/*.py") + glob.glob(f"homeassistant/components/{filesearch}/*.py")

for name in files:
    if name in [
        "homeassistant/components/sensor/__init__.py",
        "homeassistant/components/binary_sensor/__init__.py",
        "homeassistant/components/binary_sensor/device_condition.py",
        "homeassistant/components/binary_sensor/device_trigger.py",
        "homeassistant/components/button/__init__.py",
        "homeassistant/components/cover/__init__.py",
        "homeassistant/components/humidifier/__init__.py",
        "homeassistant/components/media_player/__init__.py",
        "homeassistant/components/switch/__init__.py",
        "tests/components/nest/test_sensor_sdm.py",
    ]:
        print(f" Skipping {name}.")
        continue

    with open(name) as file1:
        modified = False
        content = file1.read()
    for match, class_, enum, pkg in subs:
        strings = re.findall(re.escape(match), content)
        if len(strings) > 0:
            print(f"{name}: found '{match}'...")
            # match is in the file somewhere.  Get to work...
            import_string = f"from {pkg} import {class_}\n"
            # first get rid of it from the import line if it's the only item
            content = re.sub(
                rf"\nfrom\s+\S+\s+import\s{match}\b\n",
                rf"\n{import_string}\n",
                content,
                re.M,
            )
            # next get rid if it's a comma separated item on its own line.
            content = re.sub(
                rf"\n(from\s+\S+\s+import\s\(\n?[^\)]*)\n\s+{match}\b,?(\n[^)]*\))",
                rf"\n{import_string}\n\1\2",
                content,
                re.M,
            )
            # next get rid if it's one of a comma separated item on one line.
            content = re.sub(
                rf"\n(from\s+\S+\s+import.+){match}\b,?(.*)\n",
                rf"\n{import_string}\n\1\2\n",
                content,
                re.M,
            )

            # if type hinting for str type has been used, change to class:
            content = re.sub(
                rf"(\w+:.*)str(.*){match}",
                rf"\1{class_}\2{class_}.{enum}",
                content,
            )

            # Now the easy bit in the main body - substitute old for new
            content = re.sub(
                rf"{match}\b",
                rf"{class_}.{enum}",
                content,
            )
            # Swap any '==' for 'is'
            # Disabled because state attributes are strings:
            # https://github.com/home-assistant/core/pull/61989#discussion_r770614380
            # content = re.sub(
            #     rf"==(\s*){class_}\.{enum}\b",
            #     rf"is\1{class_}.{enum}",
            #     content,
            # )
            # Swap '==' for 'is' for sensorstateclass
            if class_ == "SensorStateClass":
                content = re.sub(
                    rf"==(\s*){class_}\.{enum}\b",
                    rf"is\1{class_}.{enum}",
                    content,
                )
            modified = True

    if modified:
        with open(
            name,
            "w",
        ) as file1:
            file1.write(content)
        isort.file(name)

    for match, _, _, _ in manualsubs:
        strings = re.findall(re.escape(match), content)
        if len(strings) > 0:
            print(f"MANUAL rework needed for {name} - {match} has more than one substitue")
            exit(1)

