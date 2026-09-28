---
title: C++ Control Flow
---

# C++ Control Flow

## Conditional Statements

Control flow structures allow your programs to make decisions and execute different code paths based on conditions.

### Basic if-else Statements

```cpp
#include <iostream>
#include <string>

void analyzeTemperature(double temperature) {
    std::string category;
    std::string recommendation;
    
    if (temperature < 0) {
        category = "Freezing";
        recommendation = "Check for ice formation";
    } else if (temperature < 10) {
        category = "Cold";
        recommendation = "Monitor equipment performance";
    } else if (temperature < 25) {
        category = "Mild";
        recommendation = "Normal operating conditions";
    } else if (temperature < 35) {
        category = "Warm";
        recommendation = "Increase ventilation";
    } else {
        category = "Hot";
        recommendation = "Critical: Check cooling systems";
    }
    
    std::cout << "Temperature: " << temperature << "°C" << std::endl;
    std::cout << "Category: " << category << std::endl;
    std::cout << "Recommendation: " << recommendation << std::endl;
}

void demonstrateBasicConditionals() {
    double readings[] = {-5.2, 8.1, 22.5, 31.8, 42.3};
    
    for (double temp : readings) {
        analyzeTemperature(temp);
        std::cout << "---" << std::endl;
    }
}
```

### Complex Conditional Logic

```cpp
#include <iostream>

void evaluateSensorData(double temperature, double humidity, double pressure) {
    bool tempNormal = (temperature >= 18.0 && temperature <= 26.0);
    bool humidityNormal = (humidity >= 40.0 && humidity <= 60.0);
    bool pressureNormal = (pressure >= 1000.0 && pressure <= 1030.0);
    
    std::cout << "Sensor Readings:" << std::endl;
    std::cout << "Temperature: " << temperature << "°C" << std::endl;
    std::cout << "Humidity: " << humidity << "%" << std::endl;
    std::cout << "Pressure: " << pressure << " hPa" << std::endl;
    
    // Complex condition evaluation
    if (tempNormal && humidityNormal && pressureNormal) {
        std::cout << "Status: All parameters normal" << std::endl;
    } else if (!tempNormal && (humidityNormal || pressureNormal)) {
        std::cout << "Warning: Temperature out of range" << std::endl;
        
        if (temperature < 18.0) {
            std::cout << "Action: Increase heating" << std::endl;
        } else {
            std::cout << "Action: Increase cooling" << std::endl;
        }
    } else if (!humidityNormal) {
        std::cout << "Warning: Humidity out of range" << std::endl;
        
        if (humidity < 40.0) {
            std::cout << "Action: Increase humidification" << std::endl;
        } else {
            std::cout << "Action: Increase dehumidification" << std::endl;
        }
    } else if (!pressureNormal) {
        std::cout << "Warning: Pressure out of range" << std::endl;
        std::cout << "Action: Check weather conditions" << std::endl;
    } else {
        std::cout << "Critical: Multiple parameters out of range" << std::endl;
        std::cout << "Action: System maintenance required" << std::endl;
    }
}
```

### Ternary Operator

```cpp
#include <iostream>
#include <algorithm>

void demonstrateTernaryOperator() {
    double values[] = {15.2, -3.8, 42.1, 0.0, 28.7};
    
    std::cout << "Ternary Operator Examples:" << std::endl;
    
    for (double value : values) {
        // Simple ternary
        std::string sign = (value >= 0) ? "positive" : "negative";
        
        // Nested ternary (use sparingly)
        std::string magnitude = (value == 0) ? "zero" : 
                               (std::abs(value) < 10) ? "small" : 
                               (std::abs(value) < 30) ? "medium" : "large";
        
        // Ternary for value selection
        double absValue = (value >= 0) ? value : -value;
        
        std::cout << "Value: " << value 
                  << " (" << sign << ", " << magnitude << ")"
                  << " Absolute: " << absValue << std::endl;
    }
    
    // Practical example: Finding min/max
    double a = 25.3, b = 18.7;
    double min = (a < b) ? a : b;
    double max = (a > b) ? a : b;
    
    std::cout << "\nMin of " << a << " and " << b << ": " << min << std::endl;
    std::cout << "Max of " << a << " and " << b << ": " << max << std::endl;
}
```

### Switch Statements

```cpp
#include <iostream>

enum class SensorType {
    TEMPERATURE,
    HUMIDITY,
    PRESSURE,
    LIGHT,
    MOTION
};

void processSensorReading(SensorType type, double value) {
    switch (type) {
        case SensorType::TEMPERATURE:
            std::cout << "Temperature sensor: " << value << "°C" << std::endl;
            if (value < 0) {
                std::cout << "Alert: Below freezing!" << std::endl;
            } else if (value > 40) {
                std::cout << "Alert: Overheating!" << std::endl;
            }
            break;
            
        case SensorType::HUMIDITY:
            std::cout << "Humidity sensor: " << value << "%" << std::endl;
            if (value < 20) {
                std::cout << "Alert: Very dry air!" << std::endl;
            } else if (value > 80) {
                std::cout << "Alert: Very humid air!" << std::endl;
            }
            break;
            
        case SensorType::PRESSURE:
            std::cout << "Pressure sensor: " << value << " hPa" << std::endl;
            if (value < 950) {
                std::cout << "Alert: Low pressure system!" << std::endl;
            } else if (value > 1050) {
                std::cout << "Alert: High pressure system!" << std::endl;
            }
            break;
            
        case SensorType::LIGHT:
            std::cout << "Light sensor: " << value << " lux" << std::endl;
            if (value < 10) {
                std::cout << "Status: Dark environment" << std::endl;
            } else if (value > 50000) {
                std::cout << "Status: Bright sunlight" << std::endl;
            }
            break;
            
        case SensorType::MOTION:
            std::cout << "Motion sensor: " << (value > 0 ? "Movement detected" : "No movement") << std::endl;
            break;
            
        default:
            std::cout << "Unknown sensor type!" << std::endl;
            break;
    }
}

void demonstrateSwitchStatement() {
    processSensorReading(SensorType::TEMPERATURE, 22.5);
    processSensorReading(SensorType::HUMIDITY, 65.0);
    processSensorReading(SensorType::PRESSURE, 1013.25);
    processSensorReading(SensorType::LIGHT, 450.0);
    processSensorReading(SensorType::MOTION, 1.0);
}
```

## Loops

### For Loops

```cpp
#include <iostream>
#include <vector>
#include <iomanip>

void demonstrateTraditionalForLoop() {
    std::vector<double> temperatures = {18.5, 19.2, 20.1, 21.8, 22.5, 21.9, 20.3};
    
    std::cout << "Daily Temperature Report:" << std::endl;
    std::cout << std::fixed << std::setprecision(1);
    
    // Traditional for loop with index
    for (int day = 0; day < temperatures.size(); ++day) {
        std::cout << "Day " << (day + 1) << ": " << temperatures[day] << "°C";
        
        // Add trend indicator
        if (day > 0) {
            double change = temperatures[day] - temperatures[day - 1];
            if (change > 0.5) {
                std::cout << " ↑ (warming)";
            } else if (change < -0.5) {
                std::cout << " ↓ (cooling)";
            } else {
                std::cout << " → (stable)";
            }
        }
        std::cout << std::endl;
    }
    
    // Calculate statistics using traditional for loop
    double sum = 0.0;
    double min = temperatures[0];
    double max = temperatures[0];
    
    for (size_t i = 0; i < temperatures.size(); ++i) {
        sum += temperatures[i];
        if (temperatures[i] < min) min = temperatures[i];
        if (temperatures[i] > max) max = temperatures[i];
    }
    
    double average = sum / temperatures.size();
    
    std::cout << "\nStatistics:" << std::endl;
    std::cout << "Average: " << average << "°C" << std::endl;
    std::cout << "Min: " << min << "°C" << std::endl;
    std::cout << "Max: " << max << "°C" << std::endl;
    std::cout << "Range: " << (max - min) << "°C" << std::endl;
}
```

### Range-Based For Loops

```cpp
#include <iostream>
#include <vector>
#include <string>

void demonstrateRangeBasedForLoops() {
    std::vector<double> sensorReadings = {12.5, 15.2, 11.8, 16.1, 13.9, 14.7, 12.3};
    std::vector<std::string> sensorNames = {"TEMP-01", "TEMP-02", "TEMP-03", "TEMP-04", 
                                           "TEMP-05", "TEMP-06", "TEMP-07"};
    
    std::cout << "Sensor Readings:" << std::endl;
    
    // Read-only access (const reference)
    for (const auto& reading : sensorReadings) {
        std::cout << "Reading: " << reading << "°C" << std::endl;
    }
    
    // Modifying elements (reference)
    std::cout << "\nApplying calibration offset (+0.5°C):" << std::endl;
    for (auto& reading : sensorReadings) {
        reading += 0.5;  // Apply calibration
        std::cout << "Calibrated: " << reading << "°C" << std::endl;
    }
    
    // Working with indices when needed
    std::cout << "\nSensor Report:" << std::endl;
    size_t index = 0;
    for (const auto& reading : sensorReadings) {
        std::cout << sensorNames[index] << ": " << reading << "°C" << std::endl;
        ++index;
    }
    
    // C++20 range-based for with init statement
    std::cout << "\nFiltered readings (> 14°C):" << std::endl;
    for (size_t i = 0; const auto& reading : sensorReadings) {
        if (reading > 14.0) {
            std::cout << sensorNames[i] << ": " << reading << "°C" << std::endl;
        }
        ++i;
    }
}
```

### While and Do-While Loops

```cpp
#include <iostream>
#include <random>
#include <vector>

void demonstrateWhileLoops() {
    // Simulate sensor data collection
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> tempDist(20.0, 2.0);  // Mean 20°C, std dev 2°C
    
    std::vector<double> readings;
    double reading;
    double sum = 0.0;
    int count = 0;
    
    std::cout << "Collecting sensor data until stable reading..." << std::endl;
    
    // While loop - may not execute if condition is false initially
    while (readings.size() < 5 || (readings.back() - (sum / count)) > 1.0) {
        reading = tempDist(gen);
        readings.push_back(reading);
        sum += reading;
        count++;
        
        double currentAverage = sum / count;
        double deviation = std::abs(reading - currentAverage);
        
        std::cout << "Reading " << count << ": " << reading << "°C" 
                  << " (avg: " << currentAverage << "°C, dev: " << deviation << "°C)" << std::endl;
        
        // Safety check to prevent infinite loop
        if (count >= 20) {
            std::cout << "Maximum readings reached." << std::endl;
            break;
        }
    }
    
    std::cout << "Final average: " << (sum / count) << "°C" << std::endl;
    
    // Do-while loop - executes at least once
    std::cout << "\nDo-while example - data validation:" << std::endl;
    double userInput;
    
    do {
        std::cout << "Enter temperature (-50 to 100°C): ";
        std::cin >> userInput;
        
        if (userInput < -50 || userInput > 100) {
            std::cout << "Invalid range! Please try again." << std::endl;
        }
    } while (userInput < -50 || userInput > 100);
    
    std::cout << "Valid temperature entered: " << userInput << "°C" << std::endl;
}
```

### Nested Loops

```cpp
#include <iostream>
#include <vector>
#include <iomanip>

void demonstrateNestedLoops() {
    // 2D temperature data (7 days, 24 hours each)
    std::vector<std::vector<double>> temperatureGrid(7, std::vector<double>(24));
    
    // Generate synthetic temperature data
    std::cout << "Generating 7-day hourly temperature data..." << std::endl;
    
    for (int day = 0; day < 7; ++day) {
        for (int hour = 0; hour < 24; ++hour) {
            // Simulate daily temperature cycle
            double baseTemp = 20.0;  // Base temperature
            double dailyVariation = 5.0 * std::sin(2 * 3.14159 * hour / 24.0);  // Daily cycle
            double weeklyTrend = (day - 3) * 0.5;  // Slight weekly trend
            double noise = (std::rand() % 100 - 50) / 100.0;  // Random noise
            
            temperatureGrid[day][hour] = baseTemp + dailyVariation + weeklyTrend + noise;
        }
    }
    
    // Display data in table format
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "\nTemperature Grid (°C):" << std::endl;
    std::cout << "Hour ";
    for (int hour = 0; hour < 24; hour += 3) {
        std::cout << std::setw(6) << hour;
    }
    std::cout << std::endl;
    
    for (int day = 0; day < 7; ++day) {
        std::cout << "Day" << (day + 1) << " ";
        for (int hour = 0; hour < 24; hour += 3) {
            std::cout << std::setw(6) << temperatureGrid[day][hour];
        }
        std::cout << std::endl;
    }
    
    // Find daily min/max temperatures
    std::cout << "\nDaily Temperature Analysis:" << std::endl;
    for (int day = 0; day < 7; ++day) {
        double dayMin = temperatureGrid[day][0];
        double dayMax = temperatureGrid[day][0];
        int minHour = 0, maxHour = 0;
        
        for (int hour = 1; hour < 24; ++hour) {
            if (temperatureGrid[day][hour] < dayMin) {
                dayMin = temperatureGrid[day][hour];
                minHour = hour;
            }
            if (temperatureGrid[day][hour] > dayMax) {
                dayMax = temperatureGrid[day][hour];
                maxHour = hour;
            }
        }
        
        std::cout << "Day " << (day + 1) << ": Min " << dayMin << "°C at " << minHour 
                  << ":00, Max " << dayMax << "°C at " << maxHour << ":00" << std::endl;
    }
}
```

## Loop Control Statements

### Break and Continue

```cpp
#include <iostream>
#include <vector>

void demonstrateLoopControl() {
    std::vector<double> dataStream = {12.5, 15.2, -999.0, 16.1, 13.9, -999.0, 14.7, 18.3, -999.0, 12.3};
    
    std::cout << "Data Processing with Break and Continue:" << std::endl;
    
    // Example 1: Using continue to skip invalid values
    std::cout << "\nValid readings (skipping -999.0 error values):" << std::endl;
    double sum = 0.0;
    int validCount = 0;
    
    for (const auto& value : dataStream) {
        if (value == -999.0) {
            std::cout << "Skipping error value" << std::endl;
            continue;  // Skip to next iteration
        }
        
        std::cout << "Processing: " << value << "°C" << std::endl;
        sum += value;
        validCount++;
    }
    
    if (validCount > 0) {
        std::cout << "Average of valid readings: " << (sum / validCount) << "°C" << std::endl;
    }
    
    // Example 2: Using break to stop on first error
    std::cout << "\nProcessing until first error:" << std::endl;
    for (size_t i = 0; i < dataStream.size(); ++i) {
        if (dataStream[i] == -999.0) {
            std::cout << "Error encountered at position " << i << ", stopping processing" << std::endl;
            break;  // Exit the loop immediately
        }
        
        std::cout << "Processed reading " << i << ": " << dataStream[i] << "°C" << std::endl;
    }
    
    // Example 3: Nested loops with labeled break simulation
    std::cout << "\nSearching 2D data for specific value:" << std::endl;
    std::vector<std::vector<int>> matrix = {
        {1, 2, 3, 4},
        {5, 6, 7, 8},
        {9, 10, 11, 12},
        {13, 14, 15, 16}
    };
    
    int target = 11;
    bool found = false;
    
    for (int row = 0; row < matrix.size() && !found; ++row) {
        for (int col = 0; col < matrix[row].size(); ++col) {
            if (matrix[row][col] == target) {
                std::cout << "Found " << target << " at position (" << row << ", " << col << ")" << std::endl;
                found = true;
                break;  // Break inner loop
            }
        }
    }
    
    if (!found) {
        std::cout << "Value " << target << " not found in matrix" << std::endl;
    }
}
```

### Advanced Loop Patterns

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

void demonstrateAdvancedLoopPatterns() {
    std::vector<double> sensorData = {12.1, 15.8, 18.3, 22.7, 19.4, 16.2, 13.9, 17.5};
    
    // Pattern 1: Processing with sliding window
    std::cout << "3-point moving average:" << std::endl;
    for (size_t i = 1; i < sensorData.size() - 1; ++i) {
        double average = (sensorData[i-1] + sensorData[i] + sensorData[i+1]) / 3.0;
        std::cout << "Position " << i << ": " << average << " (from " 
                  << sensorData[i-1] << ", " << sensorData[i] << ", " << sensorData[i+1] << ")" << std::endl;
    }
    
    // Pattern 2: Comparing adjacent elements
    std::cout << "\nTemperature changes:" << std::endl;
    for (size_t i = 1; i < sensorData.size(); ++i) {
        double change = sensorData[i] - sensorData[i-1];
        std::string trend = (change > 0) ? "↑" : (change < 0) ? "↓" : "→";
        std::cout << "Step " << (i-1) << "→" << i << ": " << change << "°C " << trend << std::endl;
    }
    
    // Pattern 3: Finding local maxima/minima
    std::cout << "\nLocal extrema:" << std::endl;
    for (size_t i = 1; i < sensorData.size() - 1; ++i) {
        bool isLocalMax = (sensorData[i] > sensorData[i-1]) && (sensorData[i] > sensorData[i+1]);
        bool isLocalMin = (sensorData[i] < sensorData[i-1]) && (sensorData[i] < sensorData[i+1]);
        
        if (isLocalMax) {
            std::cout << "Local maximum at position " << i << ": " << sensorData[i] << "°C" << std::endl;
        } else if (isLocalMin) {
            std::cout << "Local minimum at position " << i << ": " << sensorData[i] << "°C" << std::endl;
        }
    }
    
    // Pattern 4: Processing in chunks
    std::cout << "\nProcessing in chunks of 3:" << std::endl;
    for (size_t start = 0; start < sensorData.size(); start += 3) {
        size_t end = std::min(start + 3, sensorData.size());
        
        std::cout << "Chunk " << (start/3 + 1) << ": ";
        double chunkSum = 0.0;
        for (size_t i = start; i < end; ++i) {
            std::cout << sensorData[i] << " ";
            chunkSum += sensorData[i];
        }
        std::cout << "(avg: " << (chunkSum / (end - start)) << ")" << std::endl;
    }
}
```

## Next Steps

You now understand C++ control flow structures for decision making and iteration. Continue with:

- **[C++ Object-Oriented Programming](cpp-oop)** - Classes, inheritance, and polymorphism
- **[C++ Memory Management](cpp-memory-management)** - Pointers, references, and memory handling
- **[C++ Best Practices](cpp-best-practices)** - Modern C++ techniques and optimization

Control flow mastery enables you to build complex data processing algorithms and handle various sensor data scenarios!