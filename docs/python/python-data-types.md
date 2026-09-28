---
title: Python Data Types and Variables
---

# Python Data Types and Variables

## Overview

Python provides several built-in data types and collection structures that are essential for data processing. Understanding these types and their operations is crucial for effective Python programming.

## Built-in Data Types

### Numbers

```python
# Integers
integer = 42
big_integer = 1234567890123456789  # Python handles arbitrarily large integers

# Floating point numbers
floating_point = 3.14159
scientific = 1.23e-4  # Scientific notation: 0.000123

# Complex numbers
complex_number = 3 + 4j
real_part = complex_number.real      # 3.0
imaginary_part = complex_number.imag # 4.0

print(f"Integer: {integer}, type: {type(integer)}")
print(f"Float: {floating_point}, type: {type(floating_point)}")
print(f"Complex: {complex_number}, type: {type(complex_number)}")

# Number operations
result = 10 / 3        # 3.3333... (float division)
integer_div = 10 // 3  # 3 (floor division)
remainder = 10 % 3     # 1 (modulo)
power = 2 ** 8         # 256 (exponentiation)
```

### Strings

```python
# String creation
single_quotes = 'Hello'
double_quotes = "World"
multi_line = """This is a
multi-line string
spanning several lines"""

# Raw strings (useful for regex, file paths)
raw_string = r"C:\Users\name\Documents"

# String operations
name = "Python"
print(f"Length: {len(name)}")                    # 6
print(f"Uppercase: {name.upper()}")              # PYTHON
print(f"Lowercase: {name.lower()}")              # python
print(f"Capitalized: {name.capitalize()}")       # Python
print(f"Replace: {name.replace('Python', 'Programming')}")

# String methods
text = "  Hello, World!  "
print(f"Stripped: '{text.strip()}'")             # 'Hello, World!'
print(f"Split: {text.strip().split(', ')}")      # ['Hello', 'World!']
print(f"Starts with: {text.strip().startswith('Hello')}")  # True

# String formatting
temperature = 22.5
humidity = 65.2

# f-strings (recommended, Python 3.6+)
print(f"Temperature: {temperature:.1f}°C, Humidity: {humidity:.1f}%")

# .format() method
print("Temperature: {:.1f}°C, Humidity: {:.1f}%".format(temperature, humidity))

# % formatting (older style)
print("Temperature: %.1f°C, Humidity: %.1f%%" % (temperature, humidity))
```

### Boolean and None

```python
# Boolean values
is_active = True
is_complete = False

# Boolean operations
result = True and False  # False
result = True or False   # True
result = not True        # False

# None type
data = None
if data is None:
    print("No data available")

# Truthiness in Python
# False values: False, None, 0, 0.0, "", [], {}, ()
# Everything else is True
if []:
    print("This won't print")
if [1, 2, 3]:
    print("This will print")
```

## Collections

### Lists

Lists are ordered, mutable collections that can contain different data types.

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed_list = [1, "hello", 3.14, True, None]
empty_list = []

# List operations
numbers.append(6)                    # Add element at end: [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)                # Insert at position: [0, 1, 2, 3, 4, 5, 6]
numbers.remove(3)                   # Remove first occurrence: [0, 1, 2, 4, 5, 6]
popped = numbers.pop()              # Remove and return last: [0, 1, 2, 4, 5], popped=6
popped_at = numbers.pop(1)          # Remove at index: [0, 2, 4, 5], popped_at=1

# List slicing
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"First three: {data[:3]}")     # [0, 1, 2]
print(f"Last three: {data[-3:]}")     # [7, 8, 9]
print(f"Every second: {data[::2]}")   # [0, 2, 4, 6, 8]
print(f"Reversed: {data[::-1]}")      # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# List comprehensions
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
celsius_temps = [0, 10, 20, 30, 40]
fahrenheit_temps = [(c * 9/5) + 32 for c in celsius_temps]

print(f"Squares: {squares}")
print(f"Even squares: {even_squares}")
print(f"Fahrenheit: {fahrenheit_temps}")

# Nested list comprehensions
matrix = [[i*j for j in range(3)] for i in range(3)]
print(f"Matrix: {matrix}")  # [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

### Tuples

Tuples are ordered, immutable collections. They're useful for data that shouldn't change.

```python
# Creating tuples
coordinates = (3.14, 2.71)
point = ("New York", 40.7128, -74.0060)
single_item = (42,)  # Note the comma for single-item tuple

# Tuple unpacking
city, latitude, longitude = point
print(f"City: {city}, Lat: {latitude}, Lon: {longitude}")

# Multiple assignment using tuples
x, y = y, x  # Swap variables elegantly

# Named tuples for structured data
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Temperature = namedtuple('Temperature', ['value', 'unit', 'timestamp'])

p1 = Point(1, 2)
temp = Temperature(22.5, 'Celsius', '2023-10-01T10:00:00')

print(f"Point: x={p1.x}, y={p1.y}")
print(f"Temperature: {temp.value}°{temp.unit} at {temp.timestamp}")

# Tuple operations
data = (1, 2, 3, 4, 5)
print(f"Length: {len(data)}")
print(f"Max: {max(data)}")
print(f"Index of 3: {data.index(3)}")
print(f"Count of 2: {data.count(2)}")
```

### Dictionaries

Dictionaries store key-value pairs and are unordered (insertion-ordered in Python 3.7+).

```python
# Creating dictionaries
sensor_data = {
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013.25
}

# Alternative creation methods
sensor_data2 = dict(temperature=22.5, humidity=65.0, pressure=1013.25)
sensor_data3 = dict([("temperature", 22.5), ("humidity", 65.0)])

# Dictionary operations
sensor_data["timestamp"] = "2023-10-01T10:30:00"  # Add new key-value
sensor_data.update({"location": "Room A", "status": "active"})  # Add multiple

# Accessing values
temp = sensor_data["temperature"]                    # Direct access
temp = sensor_data.get("temperature", 0.0)         # Safe access with default
temp = sensor_data.get("wind_speed")               # Returns None if not found

# Dictionary methods
print(f"Keys: {list(sensor_data.keys())}")
print(f"Values: {list(sensor_data.values())}")
print(f"Items: {list(sensor_data.items())}")

# Iterating over dictionaries
for key in sensor_data:
    print(f"{key}: {sensor_data[key]}")

for key, value in sensor_data.items():
    print(f"{key}: {value}")

# Dictionary comprehensions
squared_dict = {x: x**2 for x in range(5)}
filtered_data = {k: v for k, v in sensor_data.items() if isinstance(v, (int, float))}

print(f"Squared dict: {squared_dict}")
print(f"Numeric data only: {filtered_data}")

# Nested dictionaries
weather_stations = {
    "station_001": {
        "location": "Vienna",
        "temperature": 22.5,
        "humidity": 65.0
    },
    "station_002": {
        "location": "Linz", 
        "temperature": 20.1,
        "humidity": 68.5
    }
}

vienna_temp = weather_stations["station_001"]["temperature"]
print(f"Vienna temperature: {vienna_temp}°C")
```

### Sets

Sets are unordered collections of unique elements.

```python
# Creating sets
unique_numbers = {1, 2, 3, 4, 5}
another_set = {4, 5, 6, 7, 8}
empty_set = set()  # Note: {} creates an empty dict, not set

# Set from list (removes duplicates)
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_data = set(data)  # {1, 2, 3, 4}

# Set operations
union = unique_numbers | another_set              # {1, 2, 3, 4, 5, 6, 7, 8}
intersection = unique_numbers & another_set       # {4, 5}
difference = unique_numbers - another_set         # {1, 2, 3}
symmetric_diff = unique_numbers ^ another_set     # {1, 2, 3, 6, 7, 8}

print(f"Union: {union}")
print(f"Intersection: {intersection}")
print(f"Difference: {difference}")
print(f"Symmetric difference: {symmetric_diff}")

# Set methods
unique_numbers.add(6)           # Add element
unique_numbers.discard(1)       # Remove element (no error if not present)
unique_numbers.remove(2)        # Remove element (raises error if not present)

# Set comprehensions
even_squares = {x**2 for x in range(10) if x % 2 == 0}
print(f"Even squares set: {even_squares}")
```

## Type Conversion

```python
# Converting between types
number_str = "42"
number_int = int(number_str)        # 42
number_float = float(number_str)    # 42.0

# Convert to string
age = 25
age_str = str(age)                  # "25"

# Convert collections
numbers_list = [1, 2, 3, 4, 5]
numbers_tuple = tuple(numbers_list) # (1, 2, 3, 4, 5)
numbers_set = set(numbers_list)     # {1, 2, 3, 4, 5}

# Convert string to list
text = "hello"
char_list = list(text)              # ['h', 'e', 'l', 'l', 'o']

# Split string to list
sentence = "Python is awesome"
words = sentence.split()            # ['Python', 'is', 'awesome']
```

## Practical Examples

### Data Processing with Collections

```python
# Temperature data processing example
temperature_readings = [
    {"sensor": "A", "temp": 22.5, "time": "10:00"},
    {"sensor": "B", "temp": 23.1, "time": "10:00"},
    {"sensor": "A", "temp": 22.8, "time": "10:05"},
    {"sensor": "B", "temp": 23.4, "time": "10:05"},
]

# Extract temperatures for sensor A
sensor_a_temps = [reading["temp"] for reading in temperature_readings 
                  if reading["sensor"] == "A"]

# Calculate average temperature per sensor
sensor_averages = {}
for reading in temperature_readings:
    sensor = reading["sensor"]
    temp = reading["temp"]
    
    if sensor not in sensor_averages:
        sensor_averages[sensor] = []
    sensor_averages[sensor].append(temp)

# Calculate averages
for sensor, temps in sensor_averages.items():
    avg_temp = sum(temps) / len(temps)
    print(f"Sensor {sensor} average: {avg_temp:.1f}°C")

# Find unique sensors
unique_sensors = {reading["sensor"] for reading in temperature_readings}
print(f"Active sensors: {unique_sensors}")
```

## Memory and Performance Considerations

```python
# Lists vs Tuples performance
import sys

list_data = [1, 2, 3, 4, 5]
tuple_data = (1, 2, 3, 4, 5)

print(f"List size: {sys.getsizeof(list_data)} bytes")
print(f"Tuple size: {sys.getsizeof(tuple_data)} bytes")

# When to use each collection type:
# - List: When you need to modify the collection
# - Tuple: For immutable sequences, function returns, dictionary keys
# - Dict: For key-value mappings, fast lookups
# - Set: For unique elements, fast membership testing
```

## Next Steps

Now that you understand Python's data types and collections, you're ready to explore:

- **[Control Flow](python-control-flow)** - Learn loops, conditions, and functions
- **[Object-Oriented Programming](python-oop)** - Build classes and objects
- **[File Handling](python-file-handling)** - Work with files and data persistence

These data structures form the foundation for all data processing tasks in Python!