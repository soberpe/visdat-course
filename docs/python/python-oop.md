---
title: Python Object-Oriented Programming
---

# Python Object-Oriented Programming

## Overview

Object-Oriented Programming (OOP) in Python allows you to create classes and objects that bundle data and functionality together. This approach is particularly useful for modeling real-world entities like sensors, data processors, and complex systems.

## Classes and Objects

### Basic Class Definition

```python
class TemperatureSensor:
    """A class representing a temperature sensor."""
    
    # Class variable (shared by all instances)
    sensor_count = 0
    
    def __init__(self, sensor_id, location, calibration_offset=0.0):
        """Initialize a new temperature sensor."""
        self.sensor_id = sensor_id
        self.location = location
        self.calibration_offset = calibration_offset
        self.readings = []
        
        # Increment class counter
        TemperatureSensor.sensor_count += 1
        
        print(f"Created sensor {sensor_id} at {location}")
    
    def add_reading(self, temperature):
        """Add a temperature reading."""
        calibrated_temp = temperature + self.calibration_offset
        self.readings.append(calibrated_temp)
    
    def get_average_temperature(self):
        """Calculate average temperature."""
        if not self.readings:
            return None
        return sum(self.readings) / len(self.readings)
    
    def get_reading_count(self):
        """Get number of readings."""
        return len(self.readings)
    
    def print_report(self):
        """Print a summary report."""
        print(f"\nSensor Report: {self.sensor_id}")
        print(f"Location: {self.location}")
        print(f"Readings: {self.get_reading_count()}")
        
        if self.readings:
            avg = self.get_average_temperature()
            min_temp, max_temp = min(self.readings), max(self.readings)
            print(f"Average: {avg:.1f}°C")
            print(f"Range: {min_temp:.1f}°C to {max_temp:.1f}°C")
        else:
            print("No readings available")
    
    def __str__(self):
        """String representation for users."""
        return f"TemperatureSensor({self.sensor_id}, {self.location})"
    
    def __repr__(self):
        """Developer representation."""
        return f"TemperatureSensor('{self.sensor_id}', '{self.location}', {self.calibration_offset})"

# Create and use sensors
outdoor_sensor = TemperatureSensor("OUTDOOR-01", "Garden", -0.5)
indoor_sensor = TemperatureSensor("INDOOR-01", "Living Room")

# Add readings
for temp in [15.2, 16.8, 14.9, 17.1, 15.5]:
    outdoor_sensor.add_reading(temp)

for temp in [22.1, 21.8, 22.5, 22.0, 21.9]:
    indoor_sensor.add_reading(temp)

# Print reports
outdoor_sensor.print_report()
indoor_sensor.print_report()

print(f"\nTotal sensors created: {TemperatureSensor.sensor_count}")
```

## Inheritance

### Base Classes and Derived Classes

```python
class Sensor:
    """Base class for all sensors."""
    
    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location
        self.readings = []
    
    def add_reading(self, value):
        """Add a reading (base implementation)."""
        self.readings.append(value)
    
    def get_reading_count(self):
        """Get number of readings."""
        return len(self.readings)
    
    def get_average(self):
        """Calculate average of readings."""
        if not self.readings:
            return None
        return sum(self.readings) / len(self.readings)
    
    def print_basic_info(self):
        """Print basic sensor information."""
        print(f"Sensor: {self.sensor_id} at {self.location}")
        print(f"Readings: {self.get_reading_count()}")

class TemperatureSensor(Sensor):
    """Temperature sensor with calibration."""
    
    def __init__(self, sensor_id, location, calibration_offset=0.0):
        super().__init__(sensor_id, location)  # Call parent constructor
        self.calibration_offset = calibration_offset
    
    def add_reading(self, temperature):
        """Add calibrated temperature reading."""
        calibrated_temp = temperature + self.calibration_offset
        super().add_reading(calibrated_temp)  # Call parent method
    
    def get_unit(self):
        """Return temperature unit."""
        return "°C"
    
    def print_report(self):
        """Print detailed temperature report."""
        self.print_basic_info()
        if self.readings:
            avg = self.get_average()
            print(f"Average temperature: {avg:.1f}{self.get_unit()}")

class HumiditySensor(Sensor):
    """Humidity sensor."""
    
    def get_unit(self):
        """Return humidity unit."""
        return "%RH"
    
    def print_report(self):
        """Print detailed humidity report."""
        self.print_basic_info()
        if self.readings:
            avg = self.get_average()
            print(f"Average humidity: {avg:.1f}{self.get_unit()}")

# Create different sensor types
temp_sensor = TemperatureSensor("TEMP-01", "Office", -0.2)
humidity_sensor = HumiditySensor("HUM-01", "Office")

# Add readings
temp_sensor.add_reading(22.5)
humidity_sensor.add_reading(65.0)

# Print reports
temp_sensor.print_report()
humidity_sensor.print_report()
```

## Advanced OOP Concepts

### Properties and Data Validation

```python
class ValidatedSensor:
    """Sensor with data validation using properties."""
    
    def __init__(self, sensor_id, min_value=-50, max_value=100):
        self._sensor_id = sensor_id
        self._min_value = min_value
        self._max_value = max_value
        self._readings = []
    
    @property
    def sensor_id(self):
        """Get sensor ID."""
        return self._sensor_id
    
    @sensor_id.setter
    def sensor_id(self, value):
        """Set sensor ID with validation."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Sensor ID must be a non-empty string")
        self._sensor_id = value.strip().upper()
    
    @property
    def readings(self):
        """Get copy of readings (read-only)."""
        return self._readings.copy()
    
    def add_reading(self, value):
        """Add validated reading."""
        if not isinstance(value, (int, float)):
            raise TypeError("Reading must be a number")
        
        if not (self._min_value <= value <= self._max_value):
            raise ValueError(f"Reading {value} outside valid range [{self._min_value}, {self._max_value}]")
        
        self._readings.append(value)
        print(f"Added reading: {value}")
    
    @property
    def average(self):
        """Calculate average (computed property)."""
        if not self._readings:
            return None
        return sum(self._readings) / len(self._readings)

# Usage with validation
sensor = ValidatedSensor("temp_01", -30, 50)
sensor.add_reading(25.5)  # Valid
try:
    sensor.add_reading(100)  # Will raise ValueError
except ValueError as e:
    print(f"Validation error: {e}")
```

## Next Steps

Continue with:
- **[File Handling](python-file-handling)** - Work with files and data persistence
- **[External Libraries](python-libraries)** - Leverage powerful Python libraries
- **[Programming Fundamentals](../programming/paradigms)** - Understand programming paradigms