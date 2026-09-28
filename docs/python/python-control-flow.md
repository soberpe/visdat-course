---
title: Python Control Flow
---

# Python Control Flow & Functions

## Overview

Control flow structures and functions are fundamental to Python programming. They allow you to create logic, repeat operations, and organize code into reusable components.

## Conditional Statements

### Basic if/elif/else

```python
def categorize_temperature(temp):
    """Categorize temperature reading."""
    if temp < 0:
        return "Freezing"
    elif temp < 10:
        return "Cold"
    elif temp < 25:
        return "Mild"
    elif temp < 35:
        return "Warm"
    else:
        return "Hot"

# Usage
temperature = 22.5
category = categorize_temperature(temperature)
print(f"{temperature}°C is {category}")

# Ternary operator (conditional expression)
status = "High" if temperature > 30 else "Normal"
print(f"Status: {status}")

# Complex ternary for multiple conditions
level = "Low" if temp < 20 else "Medium" if temp < 30 else "High"
```

### Multiple Conditions

```python
def check_driving_eligibility(age, has_license, has_experience=False):
    """Check if someone can drive based on multiple conditions."""
    
    if age >= 18 and has_license:
        return "Can drive independently"
    elif age >= 16 and has_license and has_experience:
        return "Can drive with supervision"
    elif age >= 16 and has_license:
        return "Can drive with adult supervision"
    else:
        return "Cannot drive"

# Test different scenarios
scenarios = [
    (25, True, True),    # Adult with license and experience
    (17, True, True),    # Minor with license and experience
    (17, True, False),   # Minor with license, no experience
    (15, False, False),  # Too young, no license
]

for age, license, experience in scenarios:
    result = check_driving_eligibility(age, license, experience)
    print(f"Age {age}, License: {license}, Experience: {experience} → {result}")
```

### Boolean Logic

```python
def validate_sensor_reading(value, min_val=-50, max_val=100, allow_none=False):
    """Validate sensor reading with multiple conditions."""
    
    # Check for None values
    if value is None:
        return allow_none
    
    # Check if value is numeric
    if not isinstance(value, (int, float)):
        return False
    
    # Check range
    if min_val <= value <= max_val:
        return True
    
    return False

# Test validation
test_values = [22.5, None, "invalid", 150, -60, 0]
for value in test_values:
    is_valid = validate_sensor_reading(value, allow_none=True)
    print(f"Value {value}: {'Valid' if is_valid else 'Invalid'}")

# Complex boolean expressions
def is_working_hours(hour, day_of_week, is_holiday=False):
    """Check if it's during working hours."""
    weekday = 0 <= day_of_week <= 4  # Monday to Friday
    business_hours = 9 <= hour <= 17
    
    return weekday and business_hours and not is_holiday

print(f"Working hours check: {is_working_hours(10, 2, False)}")  # True
print(f"Working hours check: {is_working_hours(10, 6, False)}")  # False (weekend)
```

## Loops

### For Loops

```python
# Basic iteration over sequences
measurements = [12.5, 15.2, 11.8, 16.1, 13.9]

# Iterate over values
print("Temperature readings:")
for temp in measurements:
    print(f"  {temp}°C")

# Iterate with index using enumerate
print("\nIndexed readings:")
for i, temp in enumerate(measurements):
    print(f"  Reading {i+1}: {temp}°C")

# Iterate with custom start index
print("\nCustom index start:")
for i, temp in enumerate(measurements, start=1):
    print(f"  Measurement #{i}: {temp}°C")

# Range-based loops
print("\nRange iterations:")
for i in range(5):
    print(f"Index: {i}")

# Range with start, stop, step
print("\nEven numbers 0-10:")
for i in range(0, 11, 2):
    print(f"Even number: {i}")

# Iterating over dictionaries
sensor_data = {
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013.25
}

print("\nSensor data:")
for key, value in sensor_data.items():
    print(f"{key}: {value}")

# Just keys or values
for key in sensor_data.keys():
    print(f"Sensor type: {key}")

for value in sensor_data.values():
    print(f"Reading: {value}")
```

### While Loops

```python
import random

def simulate_temperature_convergence(target=25.0, tolerance=0.1, max_iterations=100):
    """Simulate temperature converging to target value."""
    current_temp = 20.0
    iterations = 0
    
    print(f"Targeting {target}°C (±{tolerance})")
    
    while abs(current_temp - target_temp) > tolerance and iterations < max_iterations:
        # Simulate temperature change
        if current_temp < target:
            change = random.uniform(0.1, 0.8)  # Warming up
        else:
            change = random.uniform(-0.8, -0.1)  # Cooling down
            
        current_temp += change
        iterations += 1
        
        print(f"Iteration {iterations}: {current_temp:.2f}°C")
        
        # Add some random variation
        current_temp += random.uniform(-0.1, 0.1)
    
    if iterations >= max_iterations:
        print(f"Did not converge after {max_iterations} iterations")
    else:
        print(f"Converged to {current_temp:.2f}°C after {iterations} iterations")
    
    return current_temp, iterations

# Run simulation
final_temp, steps = simulate_temperature_convergence(25.0, 0.5)
```

### Loop Control

```python
def process_sensor_data(readings):
    """Process sensor data with error handling and early termination."""
    processed_count = 0
    error_count = 0
    
    for i, reading in enumerate(readings):
        # Skip None values
        if reading is None:
            print(f"  Skipping None value at index {i}")
            continue
        
        # Stop processing if too many errors
        if error_count >= 3:
            print(f"  Too many errors, stopping at index {i}")
            break
        
        # Validate reading
        if not isinstance(reading, (int, float)):
            print(f"  Error: Invalid data type at index {i}: {reading}")
            error_count += 1
            continue
        
        if not (-50 <= reading <= 100):
            print(f"  Error: Out of range value at index {i}: {reading}")
            error_count += 1
            continue
        
        # Process valid reading
        print(f"  Processing reading {i}: {reading:.1f}")
        processed_count += 1
    
    return processed_count, error_count

# Test with problematic data
test_data = [22.5, None, "invalid", 25.1, 150, 23.8, -60, 24.2, 22.0]
processed, errors = process_sensor_data(test_data)
print(f"\nSummary: {processed} processed, {errors} errors")
```

### Nested Loops

```python
def analyze_multi_sensor_data(sensor_data):
    """Analyze data from multiple sensors."""
    
    # Sample data structure: sensor_id -> list of readings
    results = {}
    
    for sensor_id, readings in sensor_data.items():
        print(f"\nAnalyzing sensor {sensor_id}:")
        
        valid_readings = []
        
        for reading in readings:
            if reading is not None and isinstance(reading, (int, float)):
                if -50 <= reading <= 100:
                    valid_readings.append(reading)
                else:
                    print(f"  Warning: Out of range reading: {reading}")
            else:
                print(f"  Warning: Invalid reading: {reading}")
        
        if valid_readings:
            avg = sum(valid_readings) / len(valid_readings)
            min_val = min(valid_readings)
            max_val = max(valid_readings)
            
            results[sensor_id] = {
                'count': len(valid_readings),
                'average': avg,
                'min': min_val,
                'max': max_val
            }
            
            print(f"  Valid readings: {len(valid_readings)}")
            print(f"  Average: {avg:.1f}")
            print(f"  Range: {min_val:.1f} to {max_val:.1f}")
        else:
            print(f"  No valid readings for sensor {sensor_id}")
    
    return results

# Test with multi-sensor data
multi_sensor_data = {
    "TEMP_01": [22.5, 23.1, 22.8, None, 23.4],
    "TEMP_02": [21.9, 22.2, "error", 21.8, 22.5],
    "TEMP_03": [150, 24.1, 24.3, 23.9]  # First reading out of range
}

analysis_results = analyze_multi_sensor_data(multi_sensor_data)
```

## Functions

### Function Basics

```python
def calculate_statistics(data):
    """
    Calculate comprehensive statistics for a dataset.
    
    Args:
        data (list): List of numerical values
        
    Returns:
        dict: Dictionary containing statistical measures
        
    Raises:
        ValueError: If data is empty or contains no valid numbers
    """
    if not data:
        raise ValueError("Cannot calculate statistics for empty dataset")
    
    # Filter out non-numeric values
    numeric_data = [x for x in data if isinstance(x, (int, float)) and x is not None]
    
    if not numeric_data:
        raise ValueError("No valid numeric values found in dataset")
    
    n = len(numeric_data)
    mean = sum(numeric_data) / n
    
    # Calculate variance and standard deviation
    variance = sum((x - mean) ** 2 for x in numeric_data) / n
    std_dev = variance ** 0.5
    
    # Sort for median calculation
    sorted_data = sorted(numeric_data)
    if n % 2 == 0:
        median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        median = sorted_data[n//2]
    
    return {
        'count': n,
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'min': min(numeric_data),
        'max': max(numeric_data),
        'range': max(numeric_data) - min(numeric_data)
    }

# Usage example
measurements = [12.5, 15.2, 11.8, 16.1, 13.9, 14.7, 12.3]
try:
    stats = calculate_statistics(measurements)
    print("Dataset Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.2f}")
        else:
            print(f"  {key}: {value}")
except ValueError as e:
    print(f"Error: {e}")
```

### Function Parameters

```python
def process_sensor_data(data, operation="mean", precision=2, verbose=False, filter_outliers=True):
    """
    Process sensor data with various configuration options.
    
    Args:
        data (list): Input sensor readings
        operation (str): Statistical operation ('mean', 'median', 'sum', 'max', 'min')
        precision (int): Decimal places for output
        verbose (bool): Whether to print detailed processing information
        filter_outliers (bool): Whether to remove outlier values
        
    Returns:
        float: Processed result
        
    Raises:
        ValueError: If operation is unknown or data is invalid
    """
    if verbose:
        print(f"Processing {len(data)} data points with operation '{operation}'")
    
    # Filter valid numeric data
    numeric_data = [x for x in data if isinstance(x, (int, float)) and x is not None]
    
    if not numeric_data:
        raise ValueError("No valid numeric data found")
    
    if verbose:
        print(f"Found {len(numeric_data)} valid readings")
    
    # Optional outlier filtering
    if filter_outliers and len(numeric_data) > 3:
        mean = sum(numeric_data) / len(numeric_data)
        std_dev = (sum((x - mean) ** 2 for x in numeric_data) / len(numeric_data)) ** 0.5
        
        # Remove values more than 2 standard deviations from mean
        filtered_data = [x for x in numeric_data if abs(x - mean) <= 2 * std_dev]
        
        if verbose and len(filtered_data) < len(numeric_data):
            print(f"Removed {len(numeric_data) - len(filtered_data)} outliers")
        
        numeric_data = filtered_data
    
    # Perform requested operation
    if operation == "mean":
        result = sum(numeric_data) / len(numeric_data)
    elif operation == "median":
        sorted_data = sorted(numeric_data)
        n = len(sorted_data)
        if n % 2 == 0:
            result = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            result = sorted_data[n//2]
    elif operation == "sum":
        result = sum(numeric_data)
    elif operation == "max":
        result = max(numeric_data)
    elif operation == "min":
        result = min(numeric_data)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return round(result, precision)

# Different ways to call the function
test_data = [1.234, 2.567, 3.891, 4.123, None, "invalid", 10.5]  # Include some bad data

# Positional arguments
result1 = process_sensor_data(test_data, "mean", 3, True, True)

# Keyword arguments
result2 = process_sensor_data(test_data, operation="median", verbose=True)

# Mixed arguments
result3 = process_sensor_data(test_data, "max", verbose=True, precision=1)

print(f"\nResults: Mean={result1}, Median={result2}, Max={result3}")
```

### Advanced Function Features

```python
def analyze_readings(*readings, **options):
    """
    Analyze multiple sensor readings with flexible parameters.
    
    Args:
        *readings: Variable number of reading lists
        **options: Keyword options (operation, precision, etc.)
    """
    operation = options.get('operation', 'mean')
    precision = options.get('precision', 2)
    verbose = options.get('verbose', False)
    
    results = []
    
    for i, reading_set in enumerate(readings):
        if verbose:
            print(f"Processing reading set {i+1}: {len(reading_set)} values")
        
        try:
            result = process_sensor_data(reading_set, operation, precision, verbose)
            results.append(result)
        except ValueError as e:
            if verbose:
                print(f"Error in set {i+1}: {e}")
            results.append(None)
    
    return results

# Usage with variable arguments
sensor_a = [22.5, 23.1, 22.8, 23.4]
sensor_b = [21.9, 22.2, 21.8, 22.5]
sensor_c = [24.1, 24.3, 23.9, 24.0]

# Analyze all sensors
results = analyze_readings(sensor_a, sensor_b, sensor_c, 
                          operation='mean', precision=1, verbose=True)

print(f"Average readings: {results}")
```

### Lambda Functions and Functional Programming

```python
# Basic lambda functions
square = lambda x: x ** 2
add = lambda x, y: x + y
celsius_to_fahrenheit = lambda c: (c * 9/5) + 32

print(f"Square of 5: {square(5)}")
print(f"25°C in Fahrenheit: {celsius_to_fahrenheit(25):.1f}°F")

# Using lambdas with built-in functions
temperatures_c = [20, 25, 30, 35, 40]

# Convert to Fahrenheit using map
temperatures_f = list(map(lambda c: (c * 9/5) + 32, temperatures_c))
print(f"Celsius: {temperatures_c}")
print(f"Fahrenheit: {temperatures_f}")

# Filter temperatures above threshold
hot_days = list(filter(lambda temp: temp > 30, temperatures_f))
print(f"Hot days (>30°C): {hot_days}")

# Sort complex data structures
sensor_readings = [
    ("Sensor_A", 22.5, "2023-10-01"),
    ("Sensor_B", 25.1, "2023-10-01"),
    ("Sensor_C", 21.8, "2023-10-01"),
    ("Sensor_A", 23.2, "2023-10-02"),
]

# Sort by temperature (second element)
sorted_by_temp = sorted(sensor_readings, key=lambda x: x[1])
print("Sorted by temperature:")
for reading in sorted_by_temp:
    print(f"  {reading[0]}: {reading[1]}°C on {reading[2]}")

# Sort by sensor name, then by temperature
sorted_by_sensor = sorted(sensor_readings, key=lambda x: (x[0], x[1]))
print("\nSorted by sensor, then temperature:")
for reading in sorted_by_sensor:
    print(f"  {reading[0]}: {reading[1]}°C on {reading[2]}")

# Using lambda with reduce for complex calculations
from functools import reduce

# Calculate product of all temperatures
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
print(f"Product of {numbers}: {product}")

# Find the reading with maximum temperature
max_reading = reduce(lambda x, y: x if x[1] > y[1] else y, sensor_readings)
print(f"Highest temperature reading: {max_reading}")
```

## Practical Examples

### Data Processing Pipeline

```python
def create_data_pipeline(*processing_functions):
    """
    Create a data processing pipeline from multiple functions.
    
    Args:
        *processing_functions: Functions to apply in sequence
        
    Returns:
        function: Pipeline function that applies all processing steps
    """
    def pipeline(data):
        result = data
        for func in processing_functions:
            result = func(result)
        return result
    
    return pipeline

# Define processing functions
def remove_none_values(data):
    """Remove None values from data."""
    return [x for x in data if x is not None]

def remove_invalid_types(data):
    """Keep only numeric values."""
    return [x for x in data if isinstance(x, (int, float))]

def remove_outliers(data, threshold=2):
    """Remove outliers beyond threshold standard deviations."""
    if len(data) < 3:
        return data
    
    mean = sum(data) / len(data)
    std_dev = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
    
    return [x for x in data if abs(x - mean) <= threshold * std_dev]

def normalize_to_range(data, target_min=0, target_max=1):
    """Normalize data to specified range."""
    if not data:
        return data
    
    data_min = min(data)
    data_max = max(data)
    
    if data_max == data_min:
        return [target_min + (target_max - target_min) / 2] * len(data)
    
    range_data = data_max - data_min
    range_target = target_max - target_min
    
    return [target_min + (x - data_min) * range_target / range_data for x in data]

# Create processing pipeline
clean_and_normalize = create_data_pipeline(
    remove_none_values,
    remove_invalid_types,
    remove_outliers,
    normalize_to_range
)

# Test with messy data
messy_data = [12.5, None, "invalid", 15.2, 11.8, 100, 16.1, 13.9, 14.7, 12.3]
print(f"Original data: {messy_data}")

cleaned_data = clean_and_normalize(messy_data)
print(f"Processed data: {[round(x, 3) for x in cleaned_data]}")
```

## Next Steps

Now that you understand Python's control flow and functions, you're ready to explore:

- **[Object-Oriented Programming](python-oop)** - Build classes and objects for complex data structures
- **[File Handling](python-file-handling)** - Work with files, CSV data, and error handling
- **[External Libraries](python-libraries)** - Leverage NumPy, Pandas for advanced data processing

These control structures and function concepts form the backbone of all Python programming!