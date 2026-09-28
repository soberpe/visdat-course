---
title: Python File Handling and I/O
---

# Python File Handling and I/O

## Overview

File handling is essential for data processing. Python provides powerful built-in capabilities for reading, writing, and processing various file formats.

## Basic File Operations

### Reading Files

```python
def read_temperature_data(filename):
    """Read temperature data from a text file."""
    temperatures = []
    
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    try:
                        temp = float(line)
                        temperatures.append(temp)
                    except ValueError:
                        print(f"Warning: Invalid data on line {line_num}: {line}")
        
        print(f"Successfully read {len(temperatures)} temperature readings")
        return temperatures
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []
    except IOError:
        print(f"Error: Could not read file '{filename}'")
        return []

# Create sample data file for testing
sample_data = """# Temperature readings (Celsius)
22.5
23.1
21.8
24.2
22.9
invalid_data
25.1
23.7
"""

with open('temperature_data.txt', 'w') as f:
    f.write(sample_data)

# Read the data
temperatures = read_temperature_data('temperature_data.txt')
if temperatures:
    avg = sum(temperatures) / len(temperatures)
    print(f"Average temperature: {avg:.1f}°C")
```

### Writing Files

```python
def save_analysis_report(data, filename, include_raw_data=True):
    """Save data analysis report to a file."""
    if not data:
        print("No data to analyze")
        return
    
    # Calculate statistics
    count = len(data)
    mean = sum(data) / count
    minimum = min(data)
    maximum = max(data)
    data_range = maximum - minimum
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in data) / count
    std_dev = variance ** 0.5
    
    with open(filename, 'w') as file:
        file.write("Data Analysis Report\n")
        file.write("=" * 20 + "\n\n")
        
        file.write(f"Dataset Summary:\n")
        file.write(f"  Number of readings: {count}\n")
        file.write(f"  Mean: {mean:.2f}\n")
        file.write(f"  Standard deviation: {std_dev:.2f}\n")
        file.write(f"  Minimum: {minimum:.2f}\n")
        file.write(f"  Maximum: {maximum:.2f}\n")
        file.write(f"  Range: {data_range:.2f}\n\n")
        
        if include_raw_data:
            file.write("Raw Data:\n")
            for i, value in enumerate(data, 1):
                file.write(f"  {i:2d}: {value:6.2f}\n")
    
    print(f"Report saved to '{filename}'")

# Generate and save report
save_analysis_report(temperatures, 'analysis_report.txt')
```

## CSV File Handling

### Reading and Writing CSV

```python
import csv

def read_sensor_data_csv(filename):
    """Read sensor data from CSV file."""
    data = []
    
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader, 1):
                try:
                    data.append({
                        'timestamp': row['timestamp'],
                        'sensor_id': row['sensor_id'],
                        'temperature': float(row['temperature']),
                        'humidity': float(row['humidity'])
                    })
                except (ValueError, KeyError) as e:
                    print(f"Error in row {row_num}: {e}")
        
        print(f"Read {len(data)} sensor readings from CSV")
        return data
        
    except FileNotFoundError:
        print(f"CSV file '{filename}' not found")
        return []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

def write_sensor_data_csv(data, filename):
    """Write sensor data to CSV file."""
    if not data:
        print("No data to write")
        return
    
    fieldnames = ['timestamp', 'sensor_id', 'temperature', 'humidity']
    
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Wrote {len(data)} records to '{filename}'")

# Create and process sample CSV data
sample_csv_data = [
    {'timestamp': '2023-10-01T10:00:00', 'sensor_id': 'TEMP01', 'temperature': 22.5, 'humidity': 65.0},
    {'timestamp': '2023-10-01T10:05:00', 'sensor_id': 'TEMP01', 'temperature': 23.1, 'humidity': 64.5},
    {'timestamp': '2023-10-01T10:10:00', 'sensor_id': 'TEMP01', 'temperature': 22.8, 'humidity': 65.2},
]

write_sensor_data_csv(sample_csv_data, 'sensor_data.csv')
csv_data = read_sensor_data_csv('sensor_data.csv')

# Analyze CSV data
temperatures_from_csv = [reading['temperature'] for reading in csv_data]
if temperatures_from_csv:
    avg_temp = sum(temperatures_from_csv) / len(temperatures_from_csv)
    print(f"Average temperature from CSV: {avg_temp:.1f}°C")
```

## Error Handling

### Custom Exceptions and Safe File Operations

```python
class DataProcessingError(Exception):
    """Base exception for data processing errors."""
    pass

class InvalidDataError(DataProcessingError):
    """Raised when data is invalid or corrupted."""
    pass

class InsufficientDataError(DataProcessingError):
    """Raised when there's not enough data for processing."""
    pass

def safe_read_numeric_file(filename, min_values=1):
    """Safely read numeric data from file with comprehensive error handling."""
    try:
        with open(filename, 'r') as file:
            data = []
            errors = []
            
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                try:
                    value = float(line)
                    
                    # Validate range (example: -100 to 100)
                    if not (-100 <= value <= 100):
                        errors.append(f"Line {line_num}: Value {value} out of valid range")
                        continue
                    
                    data.append(value)
                    
                except ValueError:
                    errors.append(f"Line {line_num}: Cannot convert '{line}' to number")
            
            # Report errors
            if errors:
                print(f"Found {len(errors)} errors:")
                for error in errors[:5]:  # Show first 5 errors
                    print(f"  {error}")
                if len(errors) > 5:
                    print(f"  ... and {len(errors) - 5} more errors")
            
            # Check if we have enough data
            if len(data) < min_values:
                raise InsufficientDataError(
                    f"Need at least {min_values} valid values, found {len(data)}"
                )
            
            print(f"Successfully loaded {len(data)} valid values")
            return data
            
    except FileNotFoundError:
        raise DataProcessingError(f"File '{filename}' not found")
    except PermissionError:
        raise DataProcessingError(f"Permission denied reading '{filename}'")
    except Exception as e:
        raise DataProcessingError(f"Unexpected error reading '{filename}': {e}")

# Usage with error handling
try:
    data = safe_read_numeric_file('temperature_data.txt', min_values=3)
    print(f"Data range: {min(data):.1f} to {max(data):.1f}")
    
except DataProcessingError as e:
    print(f"Data processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## JSON File Handling

```python
import json

def save_sensor_config(config, filename):
    """Save sensor configuration to JSON file."""
    try:
        with open(filename, 'w') as file:
            json.dump(config, file, indent=2)
        print(f"Configuration saved to {filename}")
    except Exception as e:
        print(f"Error saving configuration: {e}")

def load_sensor_config(filename):
    """Load sensor configuration from JSON file."""
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
        print(f"Configuration loaded from {filename}")
        return config
    except FileNotFoundError:
        print(f"Configuration file {filename} not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filename}: {e}")
        return None
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return None

# Example configuration
sensor_config = {
    "sensors": [
        {
            "id": "TEMP_01",
            "type": "temperature",
            "location": "Office",
            "calibration_offset": -0.2,
            "min_value": -30,
            "max_value": 50
        }
    ],
    "settings": {
        "sampling_interval": 300,
        "data_retention_days": 30
    }
}

# Save and load configuration
save_sensor_config(sensor_config, 'sensor_config.json')
loaded_config = load_sensor_config('sensor_config.json')

if loaded_config:
    print(f"Found {len(loaded_config['sensors'])} sensors in configuration")
```

## Next Steps

Continue with:
- **[External Libraries](python-libraries)** - Leverage NumPy, Pandas, and more
- **[C++ Programming](../cpp/cpp-overview)** - Learn C++ for performance-critical tasks
- **[Programming Fundamentals](../programming/paradigms)** - Understand programming paradigms