---
title: C++ Fundamentals
---

# C++ Fundamentals

## Data Types and Variables

C++ provides a rich set of built-in data types for different kinds of data processing tasks.

### Fundamental Data Types

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <limits>

void demonstrateDataTypes() {
    // Integer types
    int integer = 42;                    // Usually 32-bit
    long longInteger = 1000000L;         // At least 32-bit
    long long veryLong = 1234567890LL;   // At least 64-bit
    short shortInt = 100;                // Usually 16-bit
    
    // Unsigned variants
    unsigned int positiveOnly = 42U;
    size_t arraySize = 1000;             // For array indices and sizes
    
    // Floating-point types
    float singlePrecision = 3.14159f;    // Usually 32-bit
    double doublePrecision = 3.141592653589793; // Usually 64-bit
    long double extendedPrecision = 3.141592653589793238L;
    
    // Character types
    char character = 'A';
    unsigned char byte = 255;
    
    // Boolean type
    bool isValid = true;
    bool isEmpty = false;
    
    // String type (from standard library)
    std::string text = "Hello, Data Processing!";
    
    // Print type information
    std::cout << "Data Type Sizes:" << std::endl;
    std::cout << "int: " << sizeof(int) << " bytes" << std::endl;
    std::cout << "double: " << sizeof(double) << " bytes" << std::endl;
    std::cout << "float: " << sizeof(float) << " bytes" << std::endl;
    std::cout << "char: " << sizeof(char) << " bytes" << std::endl;
    std::cout << "bool: " << sizeof(bool) << " bytes" << std::endl;
    
    // Print value ranges
    std::cout << "\nValue Ranges:" << std::endl;
    std::cout << "int min/max: " << std::numeric_limits<int>::min() 
              << " / " << std::numeric_limits<int>::max() << std::endl;
    std::cout << "double min/max: " << std::numeric_limits<double>::min() 
              << " / " << std::numeric_limits<double>::max() << std::endl;
}
```

### Arrays and Containers

```cpp
#include <iostream>
#include <vector>
#include <array>
#include <algorithm>

void demonstrateArraysAndContainers() {
    // C-style arrays (fixed size)
    double temperatures[7] = {20.5, 22.1, 19.8, 21.3, 23.7, 18.9, 20.2};
    
    std::cout << "Temperature readings (C-array):" << std::endl;
    for (int i = 0; i < 7; ++i) {
        std::cout << "Day " << (i + 1) << ": " << temperatures[i] << "°C" << std::endl;
    }
    
    // std::array (fixed size, safer)
    std::array<double, 7> temperatureArray = {20.5, 22.1, 19.8, 21.3, 23.7, 18.9, 20.2};
    
    std::cout << "\nTemperature readings (std::array):" << std::endl;
    for (size_t i = 0; i < temperatureArray.size(); ++i) {
        std::cout << "Day " << (i + 1) << ": " << temperatureArray[i] << "°C" << std::endl;
    }
    
    // std::vector (dynamic size)
    std::vector<double> sensorReadings;
    
    // Add data
    sensorReadings.push_back(12.5);
    sensorReadings.push_back(15.2);
    sensorReadings.push_back(11.8);
    sensorReadings.push_back(16.1);
    sensorReadings.push_back(13.9);
    
    std::cout << "\nSensor readings (std::vector):" << std::endl;
    for (size_t i = 0; i < sensorReadings.size(); ++i) {
        std::cout << "Reading " << (i + 1) << ": " << sensorReadings[i] << std::endl;
    }
    
    // Range-based for loop (C++11)
    std::cout << "\nUsing range-based for loop:" << std::endl;
    for (const auto& reading : sensorReadings) {
        std::cout << "Value: " << reading << std::endl;
    }
    
    // Vector operations
    std::cout << "\nVector operations:" << std::endl;
    std::cout << "Size: " << sensorReadings.size() << std::endl;
    std::cout << "Capacity: " << sensorReadings.capacity() << std::endl;
    std::cout << "Front: " << sensorReadings.front() << std::endl;
    std::cout << "Back: " << sensorReadings.back() << std::endl;
    
    // Find minimum and maximum
    auto minElement = std::min_element(sensorReadings.begin(), sensorReadings.end());
    auto maxElement = std::max_element(sensorReadings.begin(), sensorReadings.end());
    
    std::cout << "Min: " << *minElement << std::endl;
    std::cout << "Max: " << *maxElement << std::endl;
}
```

### Constants and Type Qualifiers

```cpp
#include <iostream>

void demonstrateConstants() {
    // const keyword
    const double PI = 3.141592653589793;
    const int MAX_SENSORS = 100;
    
    // constexpr (compile-time constants)
    constexpr double EARTH_GRAVITY = 9.81;
    constexpr int SECONDS_PER_HOUR = 3600;
    
    // const with pointers
    const double* constDataPtr = &PI;        // Pointer to const data
    double* const ptrToConst = nullptr;      // Const pointer (cannot be reassigned)
    const double* const constPtrToConst = &PI; // Const pointer to const data
    
    // Read-only parameter
    auto printValue = [](const double& value) {
        std::cout << "Value: " << value << std::endl;
        // value = 10.0; // Error: cannot modify const parameter
    };
    
    printValue(PI);
    
    std::cout << "Constants:" << std::endl;
    std::cout << "PI: " << PI << std::endl;
    std::cout << "Earth gravity: " << EARTH_GRAVITY << " m/s²" << std::endl;
    std::cout << "Seconds per hour: " << SECONDS_PER_HOUR << std::endl;
}
```

## Operators

### Arithmetic Operators

```cpp
#include <iostream>
#include <cmath>

void demonstrateArithmeticOperators() {
    double a = 15.5;
    double b = 4.2;
    
    std::cout << "Arithmetic Operations:" << std::endl;
    std::cout << "a = " << a << ", b = " << b << std::endl;
    std::cout << "a + b = " << (a + b) << std::endl;
    std::cout << "a - b = " << (a - b) << std::endl;
    std::cout << "a * b = " << (a * b) << std::endl;
    std::cout << "a / b = " << (a / b) << std::endl;
    
    // Integer division vs floating-point division
    int intA = 15;
    int intB = 4;
    std::cout << "\nInteger vs Float Division:" << std::endl;
    std::cout << intA << " / " << intB << " = " << (intA / intB) << " (integer)" << std::endl;
    std::cout << intA << " / " << intB << " = " << (static_cast<double>(intA) / intB) << " (float)" << std::endl;
    
    // Modulo operator
    std::cout << intA << " % " << intB << " = " << (intA % intB) << std::endl;
    
    // Compound assignment operators
    double c = 10.0;
    std::cout << "\nCompound Assignment:" << std::endl;
    std::cout << "c = " << c << std::endl;
    
    c += 5.0;  // c = c + 5.0
    std::cout << "c += 5.0: " << c << std::endl;
    
    c *= 2.0;  // c = c * 2.0
    std::cout << "c *= 2.0: " << c << std::endl;
    
    c /= 3.0;  // c = c / 3.0
    std::cout << "c /= 3.0: " << c << std::endl;
    
    // Increment and decrement
    int counter = 5;
    std::cout << "\nIncrement/Decrement:" << std::endl;
    std::cout << "counter = " << counter << std::endl;
    std::cout << "++counter = " << (++counter) << std::endl;  // Pre-increment
    std::cout << "counter++ = " << (counter++) << std::endl;  // Post-increment
    std::cout << "final counter = " << counter << std::endl;
}
```

### Comparison and Logical Operators

```cpp
#include <iostream>

void demonstrateComparisonOperators() {
    double temperature = 22.5;
    double humidity = 65.0;
    
    std::cout << "Comparison Operations:" << std::endl;
    std::cout << "Temperature: " << temperature << "°C" << std::endl;
    std::cout << "Humidity: " << humidity << "%" << std::endl;
    
    // Comparison operators
    std::cout << "\nComparisons:" << std::endl;
    std::cout << "Temperature > 20: " << (temperature > 20) << std::endl;
    std::cout << "Temperature < 25: " << (temperature < 25) << std::endl;
    std::cout << "Temperature >= 22.5: " << (temperature >= 22.5) << std::endl;
    std::cout << "Temperature <= 22.0: " << (temperature <= 22.0) << std::endl;
    std::cout << "Temperature == 22.5: " << (temperature == 22.5) << std::endl;
    std::cout << "Temperature != 25.0: " << (temperature != 25.0) << std::endl;
    
    // Logical operators
    bool isComfortable = (temperature >= 20.0 && temperature <= 25.0) && 
                        (humidity >= 40.0 && humidity <= 70.0);
    
    bool needsAttention = temperature < 10.0 || temperature > 35.0 || 
                         humidity < 20.0 || humidity > 80.0;
    
    std::cout << "\nLogical Operations:" << std::endl;
    std::cout << "Is comfortable: " << isComfortable << std::endl;
    std::cout << "Needs attention: " << needsAttention << std::endl;
    std::cout << "Not comfortable: " << (!isComfortable) << std::endl;
}
```

### Bitwise Operators

```cpp
#include <iostream>
#include <bitset>

void demonstrateBitwiseOperators() {
    unsigned int a = 12;  // Binary: 1100
    unsigned int b = 10;  // Binary: 1010
    
    std::cout << "Bitwise Operations:" << std::endl;
    std::cout << "a = " << a << " (binary: " << std::bitset<8>(a) << ")" << std::endl;
    std::cout << "b = " << b << " (binary: " << std::bitset<8>(b) << ")" << std::endl;
    
    // Bitwise operators
    std::cout << "\nResults:" << std::endl;
    std::cout << "a & b = " << (a & b) << " (binary: " << std::bitset<8>(a & b) << ")" << std::endl;  // AND
    std::cout << "a | b = " << (a | b) << " (binary: " << std::bitset<8>(a | b) << ")" << std::endl;  // OR
    std::cout << "a ^ b = " << (a ^ b) << " (binary: " << std::bitset<8>(a ^ b) << ")" << std::endl;  // XOR
    std::cout << "~a = " << (~a) << " (binary: " << std::bitset<8>(~a) << ")" << std::endl;           // NOT
    std::cout << "a << 2 = " << (a << 2) << " (binary: " << std::bitset<8>(a << 2) << ")" << std::endl; // Left shift
    std::cout << "a >> 1 = " << (a >> 1) << " (binary: " << std::bitset<8>(a >> 1) << ")" << std::endl; // Right shift
    
    // Practical example: Bit flags for sensor status
    const unsigned int TEMP_SENSOR_OK = 1;      // Bit 0
    const unsigned int HUMIDITY_SENSOR_OK = 2;  // Bit 1
    const unsigned int PRESSURE_SENSOR_OK = 4;  // Bit 2
    const unsigned int GPS_SENSOR_OK = 8;       // Bit 3
    
    unsigned int sensorStatus = 0;
    
    // Set sensor status
    sensorStatus |= TEMP_SENSOR_OK;      // Turn on temperature sensor
    sensorStatus |= HUMIDITY_SENSOR_OK;  // Turn on humidity sensor
    sensorStatus |= GPS_SENSOR_OK;       // Turn on GPS sensor
    
    std::cout << "\nSensor Status Example:" << std::endl;
    std::cout << "Status: " << std::bitset<8>(sensorStatus) << std::endl;
    std::cout << "Temperature sensor OK: " << ((sensorStatus & TEMP_SENSOR_OK) != 0) << std::endl;
    std::cout << "Humidity sensor OK: " << ((sensorStatus & HUMIDITY_SENSOR_OK) != 0) << std::endl;
    std::cout << "Pressure sensor OK: " << ((sensorStatus & PRESSURE_SENSOR_OK) != 0) << std::endl;
    std::cout << "GPS sensor OK: " << ((sensorStatus & GPS_SENSOR_OK) != 0) << std::endl;
}
```

## Type Conversion and Casting

### Implicit Conversions

```cpp
#include <iostream>

void demonstrateImplicitConversions() {
    std::cout << "Implicit Type Conversions:" << std::endl;
    
    // Numeric promotions
    int intValue = 42;
    double doubleValue = 3.14159;
    
    // int promoted to double
    double result = intValue + doubleValue;
    std::cout << intValue << " + " << doubleValue << " = " << result << std::endl;
    
    // Potential precision loss
    int truncated = doubleValue;  // Warning: possible loss of data
    std::cout << "double " << doubleValue << " truncated to int: " << truncated << std::endl;
    
    // Character to numeric conversions
    char digit = '5';
    int digitValue = digit - '0';  // Convert char digit to int
    std::cout << "Character '" << digit << "' as integer: " << digitValue << std::endl;
    
    // Boolean conversions
    bool fromInt = 42;     // Non-zero becomes true
    bool fromZero = 0;     // Zero becomes false
    int fromTrue = true;   // true becomes 1
    int fromFalse = false; // false becomes 0
    
    std::cout << "42 as bool: " << fromInt << std::endl;
    std::cout << "0 as bool: " << fromZero << std::endl;
    std::cout << "true as int: " << fromTrue << std::endl;
    std::cout << "false as int: " << fromFalse << std::endl;
}
```

### Explicit Casting

```cpp
#include <iostream>
#include <string>

void demonstrateExplicitCasting() {
    std::cout << "Explicit Type Casting:" << std::endl;
    
    // C-style cast (avoid in modern C++)
    double pi = 3.14159;
    int piInt = (int)pi;
    std::cout << "C-style cast: " << pi << " -> " << piInt << std::endl;
    
    // static_cast (compile-time conversion)
    double value = 42.7;
    int intValue = static_cast<int>(value);
    std::cout << "static_cast: " << value << " -> " << intValue << std::endl;
    
    // Convert between numeric types safely
    float floatValue = static_cast<float>(pi);
    std::cout << "double to float: " << pi << " -> " << floatValue << std::endl;
    
    // dynamic_cast (runtime type checking for polymorphic types)
    // (Example would require inheritance hierarchy)
    
    // const_cast (remove const qualifier - use with caution)
    const int constValue = 100;
    int* nonConstPtr = const_cast<int*>(&constValue);
    std::cout << "const_cast: removed const from " << constValue << std::endl;
    
    // reinterpret_cast (low-level reinterpretation - dangerous)
    int number = 0x41424344;  // ASCII "ABCD"
    char* charPtr = reinterpret_cast<char*>(&number);
    std::cout << "reinterpret_cast: ";
    for (int i = 0; i < 4; ++i) {
        std::cout << charPtr[i];
    }
    std::cout << std::endl;
}
```

## Variable Scope and Lifetime

```cpp
#include <iostream>

int globalVariable = 100;  // Global scope

void demonstrateScope() {
    int localVariable = 200;  // Function scope
    
    std::cout << "Global variable: " << globalVariable << std::endl;
    std::cout << "Local variable: " << localVariable << std::endl;
    
    // Block scope
    {
        int blockVariable = 300;  // Block scope
        int localVariable = 400;  // Shadows outer localVariable
        
        std::cout << "Block variable: " << blockVariable << std::endl;
        std::cout << "Local variable (shadowed): " << localVariable << std::endl;
        std::cout << "Global variable: " << globalVariable << std::endl;
    }
    // blockVariable is out of scope here
    
    std::cout << "Local variable (after block): " << localVariable << std::endl;
    
    // Static variables
    for (int i = 0; i < 3; ++i) {
        static int staticCounter = 0;  // Initialized only once
        int autoCounter = 0;           // Initialized each iteration
        
        staticCounter++;
        autoCounter++;
        
        std::cout << "Iteration " << i << ": static=" << staticCounter 
                  << ", auto=" << autoCounter << std::endl;
    }
}
```

## Next Steps

You now understand C++ fundamentals including data types, operators, and variable scope. Continue with:

- **[C++ Control Flow](cpp-control-flow)** - Conditional statements and loops
- **[C++ Object-Oriented Programming](cpp-oop)** - Classes and inheritance
- **[C++ Memory Management](cpp-memory-management)** - Pointers and memory handling
- **[C++ Best Practices](cpp-best-practices)** - Modern C++ techniques

These fundamentals form the foundation for all C++ programming in data processing applications!