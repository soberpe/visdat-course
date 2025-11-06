---
title: Programming Paradigms
---

# Programming Paradigms

## Introduction

Programming paradigms are fundamental styles of programming that provide different approaches to organizing and structuring code. Understanding these paradigms helps you choose the right tool for the task and write more effective code.

## Imperative Programming

### Procedural Programming

Procedural programming organizes code into procedures (functions) that operate on data.

```python
# Python procedural example
def calculate_sensor_statistics(readings):
    """Calculate basic statistics for sensor readings."""
    if not readings:
        return None
    
    total = sum(readings)
    mean = total / len(readings)
    
    sorted_readings = sorted(readings)
    n = len(sorted_readings)
    median = (sorted_readings[n//2 - 1] + sorted_readings[n//2]) / 2 if n % 2 == 0 else sorted_readings[n//2]
    
    variance = sum((x - mean) ** 2 for x in readings) / len(readings)
    std_dev = variance ** 0.5
    
    return {
        'count': len(readings),
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'min': min(readings),
        'max': max(readings)
    }

def process_sensor_data(sensor_data):
    """Process multiple sensor datasets."""
    results = {}
    
    for sensor_id, readings in sensor_data.items():
        print(f"Processing sensor {sensor_id}...")
        stats = calculate_sensor_statistics(readings)
        
        if stats:
            results[sensor_id] = stats
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Range: {stats['min']:.2f} to {stats['max']:.2f}")
        else:
            print(f"  No valid data for sensor {sensor_id}")
    
    return results

# Example usage
sensor_data = {
    'TEMP_01': [22.5, 23.1, 21.8, 24.2, 22.9],
    'TEMP_02': [19.3, 20.1, 18.7, 21.0, 19.8],
    'TEMP_03': []  # Empty dataset
}

results = process_sensor_data(sensor_data)
```

```cpp
// C++ procedural example
#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <numeric>
#include <cmath>
#include <iostream>

struct SensorStats {
    size_t count;
    double mean;
    double median;
    double std_dev;
    double min_val;
    double max_val;
};

std::optional<SensorStats> calculateSensorStatistics(const std::vector<double>& readings) {
    if (readings.empty()) {
        return std::nullopt;
    }
    
    // Calculate mean
    double sum = std::accumulate(readings.begin(), readings.end(), 0.0);
    double mean = sum / readings.size();
    
    // Calculate median
    std::vector<double> sorted_readings = readings;
    std::sort(sorted_readings.begin(), sorted_readings.end());
    
    double median;
    size_t n = sorted_readings.size();
    if (n % 2 == 0) {
        median = (sorted_readings[n/2 - 1] + sorted_readings[n/2]) / 2.0;
    } else {
        median = sorted_readings[n/2];
    }
    
    // Calculate standard deviation
    double variance = 0.0;
    for (const auto& reading : readings) {
        variance += (reading - mean) * (reading - mean);
    }
    variance /= readings.size();
    double std_dev = std::sqrt(variance);
    
    // Find min and max
    auto [min_it, max_it] = std::minmax_element(readings.begin(), readings.end());
    
    return SensorStats{
        readings.size(),
        mean,
        median,
        std_dev,
        *min_it,
        *max_it
    };
}

std::map<std::string, SensorStats> processSensorData(
    const std::map<std::string, std::vector<double>>& sensorData) {
    
    std::map<std::string, SensorStats> results;
    
    for (const auto& [sensorId, readings] : sensorData) {
        std::cout << "Processing sensor " << sensorId << "..." << std::endl;
        
        if (auto stats = calculateSensorStatistics(readings)) {
            results[sensorId] = *stats;
            std::cout << "  Mean: " << stats->mean << std::endl;
            std::cout << "  Range: " << stats->min_val << " to " << stats->max_val << std::endl;
        } else {
            std::cout << "  No valid data for sensor " << sensorId << std::endl;
        }
    }
    
    return results;
}
```

### Structured Programming

Structured programming emphasizes clean control flow and modularity.

```python
# Python structured programming example
class DataValidator:
    @staticmethod
    def validate_temperature(value):
        """Validate temperature reading."""
        return -50 <= value <= 100
    
    @staticmethod
    def validate_humidity(value):
        """Validate humidity reading."""
        return 0 <= value <= 100
    
    @staticmethod
    def validate_pressure(value):
        """Validate pressure reading."""
        return 800 <= value <= 1200

def clean_sensor_data(raw_data, validator_func):
    """Clean sensor data using provided validator."""
    cleaned_data = []
    invalid_count = 0
    
    for reading in raw_data:
        if validator_func(reading):
            cleaned_data.append(reading)
        else:
            invalid_count += 1
    
    return cleaned_data, invalid_count

def process_sensor_batch(sensor_batch):
    """Process a batch of sensor data with validation."""
    results = {}
    
    for sensor_type, data in sensor_batch.items():
        print(f"\nProcessing {sensor_type} data:")
        
        # Select appropriate validator
        if sensor_type == 'temperature':
            validator = DataValidator.validate_temperature
        elif sensor_type == 'humidity':
            validator = DataValidator.validate_humidity
        elif sensor_type == 'pressure':
            validator = DataValidator.validate_pressure
        else:
            print(f"  Unknown sensor type: {sensor_type}")
            continue
        
        # Clean and process data
        cleaned_data, invalid_count = clean_sensor_data(data, validator)
        
        if cleaned_data:
            stats = calculate_sensor_statistics(cleaned_data)
            results[sensor_type] = {
                'stats': stats,
                'valid_readings': len(cleaned_data),
                'invalid_readings': invalid_count
            }
            
            print(f"  Valid readings: {len(cleaned_data)}")
            print(f"  Invalid readings: {invalid_count}")
            print(f"  Mean: {stats['mean']:.2f}")
        else:
            print(f"  No valid data after cleaning")
    
    return results

# Example usage
sensor_batch = {
    'temperature': [22.5, 150, 23.1, -100, 21.8, 24.2],  # Contains invalid data
    'humidity': [65, 45, 120, 38, 52, -10, 48],          # Contains invalid data
    'pressure': [1013, 1015, 2000, 1010, 500, 1012]     # Contains invalid data
}

batch_results = process_sensor_batch(sensor_batch)
```

## Object-Oriented Programming

### Encapsulation and Abstraction

```python
# Python OOP example
from abc import ABC, abstractmethod
from typing import List, Optional
import time

class Sensor(ABC):
    """Abstract base class for all sensors."""
    
    def __init__(self, sensor_id: str):
        self._sensor_id = sensor_id
        self._readings: List[float] = []
        self._last_reading_time: Optional[float] = None
        self._is_active = True
    
    @property
    def sensor_id(self) -> str:
        return self._sensor_id
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def activate(self):
        """Activate the sensor."""
        self._is_active = True
        print(f"Sensor {self._sensor_id} activated")
    
    def deactivate(self):
        """Deactivate the sensor."""
        self._is_active = False
        print(f"Sensor {self._sensor_id} deactivated")
    
    @abstractmethod
    def read_raw_value(self) -> float:
        """Read raw value from sensor. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def calibrate_reading(self, raw_value: float) -> float:
        """Calibrate raw reading. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def get_unit(self) -> str:
        """Get measurement unit. Must be implemented by subclasses."""
        pass
    
    def take_reading(self) -> Optional[float]:
        """Take a calibrated reading from the sensor."""
        if not self._is_active:
            print(f"Sensor {self._sensor_id} is not active")
            return None
        
        try:
            raw_value = self.read_raw_value()
            calibrated_value = self.calibrate_reading(raw_value)
            
            self._readings.append(calibrated_value)
            self._last_reading_time = time.time()
            
            print(f"{self._sensor_id}: {calibrated_value:.2f} {self.get_unit()}")
            return calibrated_value
            
        except Exception as e:
            print(f"Error reading from sensor {self._sensor_id}: {e}")
            return None
    
    def get_recent_readings(self, count: int = 10) -> List[float]:
        """Get the most recent readings."""
        return self._readings[-count:] if self._readings else []
    
    def get_average(self) -> Optional[float]:
        """Calculate average of all readings."""
        if not self._readings:
            return None
        return sum(self._readings) / len(self._readings)

class TemperatureSensor(Sensor):
    """Temperature sensor implementation."""
    
    def __init__(self, sensor_id: str, calibration_offset: float = 0.0):
        super().__init__(sensor_id)
        self._calibration_offset = calibration_offset
    
    def read_raw_value(self) -> float:
        # Simulate temperature reading
        import random
        return 20.0 + random.uniform(-5, 10)
    
    def calibrate_reading(self, raw_value: float) -> float:
        return raw_value + self._calibration_offset
    
    def get_unit(self) -> str:
        return "°C"

class HumiditySensor(Sensor):
    """Humidity sensor implementation."""
    
    def __init__(self, sensor_id: str, calibration_factor: float = 1.0):
        super().__init__(sensor_id)
        self._calibration_factor = calibration_factor
    
    def read_raw_value(self) -> float:
        # Simulate humidity reading
        import random
        return random.uniform(30, 80)
    
    def calibrate_reading(self, raw_value: float) -> float:
        return raw_value * self._calibration_factor
    
    def get_unit(self) -> str:
        return "%"

class SensorNetwork:
    """Manages a network of sensors."""
    
    def __init__(self):
        self._sensors: List[Sensor] = []
    
    def add_sensor(self, sensor: Sensor):
        """Add a sensor to the network."""
        self._sensors.append(sensor)
        print(f"Added sensor {sensor.sensor_id} to network")
    
    def remove_sensor(self, sensor_id: str) -> bool:
        """Remove a sensor from the network."""
        for i, sensor in enumerate(self._sensors):
            if sensor.sensor_id == sensor_id:
                del self._sensors[i]
                print(f"Removed sensor {sensor_id} from network")
                return True
        return False
    
    def take_all_readings(self):
        """Take readings from all active sensors."""
        print("Taking readings from all sensors:")
        for sensor in self._sensors:
            if sensor.is_active:
                sensor.take_reading()
    
    def get_network_summary(self):
        """Get summary of all sensors in the network."""
        print("\nNetwork Summary:")
        for sensor in self._sensors:
            avg = sensor.get_average()
            status = "Active" if sensor.is_active else "Inactive"
            readings_count = len(sensor.get_recent_readings(1000))
            
            print(f"  {sensor.sensor_id}: {status}, "
                  f"{readings_count} readings, "
                  f"avg: {avg:.2f if avg else 'N/A'} {sensor.get_unit()}")

# Example usage
def demonstrate_oop():
    # Create sensor network
    network = SensorNetwork()
    
    # Add sensors
    temp1 = TemperatureSensor("TEMP-01", calibration_offset=-0.5)
    temp2 = TemperatureSensor("TEMP-02", calibration_offset=0.2)
    humidity1 = HumiditySensor("HUM-01", calibration_factor=0.95)
    
    network.add_sensor(temp1)
    network.add_sensor(temp2)
    network.add_sensor(humidity1)
    
    # Take several readings
    for i in range(5):
        print(f"\nReading cycle {i+1}:")
        network.take_all_readings()
    
    # Deactivate one sensor
    temp2.deactivate()
    
    print(f"\nAfter deactivating {temp2.sensor_id}:")
    network.take_all_readings()
    
    # Show network summary
    network.get_network_summary()

if __name__ == "__main__":
    demonstrate_oop()
```

### Inheritance and Polymorphism

```cpp
// C++ OOP example with inheritance and polymorphism
#include <iostream>
#include <vector>
#include <memory>
#include <string>
#include <algorithm>
#include <chrono>
#include <random>

class Sensor {
protected:
    std::string m_sensorId;
    std::vector<double> m_readings;
    bool m_isActive;
    std::chrono::system_clock::time_point m_lastReadingTime;
    
public:
    explicit Sensor(const std::string& sensorId) 
        : m_sensorId(sensorId), m_isActive(true) {}
    
    virtual ~Sensor() = default;
    
    // Pure virtual methods (abstract interface)
    virtual double readRawValue() = 0;
    virtual double calibrateReading(double rawValue) = 0;
    virtual std::string getUnit() const = 0;
    virtual std::string getSensorType() const = 0;
    
    // Common functionality
    virtual std::optional<double> takeReading() {
        if (!m_isActive) {
            std::cout << "Sensor " << m_sensorId << " is not active" << std::endl;
            return std::nullopt;
        }
        
        try {
            double rawValue = readRawValue();
            double calibratedValue = calibrateReading(rawValue);
            
            m_readings.push_back(calibratedValue);
            m_lastReadingTime = std::chrono::system_clock::now();
            
            std::cout << m_sensorId << ": " << calibratedValue << " " << getUnit() << std::endl;
            return calibratedValue;
            
        } catch (const std::exception& e) {
            std::cout << "Error reading from sensor " << m_sensorId << ": " << e.what() << std::endl;
            return std::nullopt;
        }
    }
    
    void activate() {
        m_isActive = true;
        std::cout << "Sensor " << m_sensorId << " activated" << std::endl;
    }
    
    void deactivate() {
        m_isActive = false;
        std::cout << "Sensor " << m_sensorId << " deactivated" << std::endl;
    }
    
    std::vector<double> getRecentReadings(size_t count = 10) const {
        if (m_readings.size() <= count) {
            return m_readings;
        }
        return std::vector<double>(m_readings.end() - count, m_readings.end());
    }
    
    std::optional<double> getAverage() const {
        if (m_readings.empty()) {
            return std::nullopt;
        }
        
        double sum = 0.0;
        for (const auto& reading : m_readings) {
            sum += reading;
        }
        return sum / m_readings.size();
    }
    
    // Getters
    const std::string& getSensorId() const { return m_sensorId; }
    bool isActive() const { return m_isActive; }
    size_t getReadingCount() const { return m_readings.size(); }
};

class TemperatureSensor : public Sensor {
private:
    double m_calibrationOffset;
    std::mt19937 m_generator;
    std::uniform_real_distribution<double> m_distribution;
    
public:
    TemperatureSensor(const std::string& sensorId, double calibrationOffset = 0.0)
        : Sensor(sensorId), m_calibrationOffset(calibrationOffset),
          m_generator(std::random_device{}()), m_distribution(-5.0, 10.0) {}
    
    double readRawValue() override {
        // Simulate temperature reading
        return 20.0 + m_distribution(m_generator);
    }
    
    double calibrateReading(double rawValue) override {
        return rawValue + m_calibrationOffset;
    }
    
    std::string getUnit() const override {
        return "°C";
    }
    
    std::string getSensorType() const override {
        return "Temperature";
    }
};

class HumiditySensor : public Sensor {
private:
    double m_calibrationFactor;
    std::mt19937 m_generator;
    std::uniform_real_distribution<double> m_distribution;
    
public:
    HumiditySensor(const std::string& sensorId, double calibrationFactor = 1.0)
        : Sensor(sensorId), m_calibrationFactor(calibrationFactor),
          m_generator(std::random_device{}()), m_distribution(30.0, 80.0) {}
    
    double readRawValue() override {
        // Simulate humidity reading
        return m_distribution(m_generator);
    }
    
    double calibrateReading(double rawValue) override {
        return rawValue * m_calibrationFactor;
    }
    
    std::string getUnit() const override {
        return "%";
    }
    
    std::string getSensorType() const override {
        return "Humidity";
    }
};

class SensorNetwork {
private:
    std::vector<std::unique_ptr<Sensor>> m_sensors;
    
public:
    void addSensor(std::unique_ptr<Sensor> sensor) {
        std::cout << "Added sensor " << sensor->getSensorId() << " to network" << std::endl;
        m_sensors.push_back(std::move(sensor));
    }
    
    bool removeSensor(const std::string& sensorId) {
        auto it = std::find_if(m_sensors.begin(), m_sensors.end(),
                              [&sensorId](const auto& sensor) {
                                  return sensor->getSensorId() == sensorId;
                              });
        
        if (it != m_sensors.end()) {
            std::cout << "Removed sensor " << sensorId << " from network" << std::endl;
            m_sensors.erase(it);
            return true;
        }
        return false;
    }
    
    void takeAllReadings() {
        std::cout << "Taking readings from all sensors:" << std::endl;
        for (auto& sensor : m_sensors) {
            if (sensor->isActive()) {
                sensor->takeReading();
            }
        }
    }
    
    void getNetworkSummary() const {
        std::cout << "\nNetwork Summary:" << std::endl;
        for (const auto& sensor : m_sensors) {
            auto avg = sensor->getAverage();
            std::string status = sensor->isActive() ? "Active" : "Inactive";
            
            std::cout << "  " << sensor->getSensorId() << ": " << status
                      << ", " << sensor->getReadingCount() << " readings"
                      << ", avg: ";
            
            if (avg) {
                std::cout << *avg;
            } else {
                std::cout << "N/A";
            }
            std::cout << " " << sensor->getUnit() << std::endl;
        }
    }
    
    std::vector<Sensor*> getSensorsByType(const std::string& type) const {
        std::vector<Sensor*> result;
        for (const auto& sensor : m_sensors) {
            if (sensor->getSensorType() == type) {
                result.push_back(sensor.get());
            }
        }
        return result;
    }
};

void demonstrateCppOOP() {
    std::cout << "=== C++ OOP Demonstration ===" << std::endl;
    
    // Create sensor network
    SensorNetwork network;
    
    // Add sensors
    network.addSensor(std::make_unique<TemperatureSensor>("TEMP-01", -0.5));
    network.addSensor(std::make_unique<TemperatureSensor>("TEMP-02", 0.2));
    network.addSensor(std::make_unique<HumiditySensor>("HUM-01", 0.95));
    
    // Take several readings
    for (int i = 0; i < 5; ++i) {
        std::cout << "\nReading cycle " << (i + 1) << ":" << std::endl;
        network.takeAllReadings();
    }
    
    // Demonstrate polymorphism
    std::cout << "\nDemonstrating polymorphism:" << std::endl;
    auto tempSensors = network.getSensorsByType("Temperature");
    std::cout << "Found " << tempSensors.size() << " temperature sensors" << std::endl;
    
    // Show network summary
    network.getNetworkSummary();
}
```

## Functional Programming

### Higher-Order Functions and Immutability

```python
# Python functional programming example
from functools import reduce, partial
from typing import List, Callable, Tuple
import operator

# Pure functions (no side effects)
def normalize_reading(value: float, min_val: float, max_val: float) -> float:
    """Normalize a reading to 0-1 range."""
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)

def apply_calibration(reading: float, offset: float, scale: float) -> float:
    """Apply calibration to a reading."""
    return (reading + offset) * scale

# Higher-order functions
def create_filter(min_val: float, max_val: float) -> Callable[[float], bool]:
    """Create a filter function for valid readings."""
    return lambda x: min_val <= x <= max_val

def create_calibrator(offset: float, scale: float) -> Callable[[float], float]:
    """Create a calibration function."""
    return partial(apply_calibration, offset=offset, scale=scale)

def compose_functions(*functions):
    """Compose multiple functions into one."""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

# Functional data processing pipeline
def process_sensor_data_functional(
    raw_readings: List[float],
    calibrator: Callable[[float], float],
    validator: Callable[[float], bool],
    transformer: Callable[[float], float] = lambda x: x
) -> Tuple[List[float], List[float]]:
    """Process sensor data using functional approach."""
    
    # Apply calibration
    calibrated = list(map(calibrator, raw_readings))
    
    # Separate valid and invalid readings
    valid_readings = list(filter(validator, calibrated))
    invalid_readings = [x for x in calibrated if not validator(x)]
    
    # Apply transformation
    transformed = list(map(transformer, valid_readings))
    
    return transformed, invalid_readings

def calculate_statistics_functional(readings: List[float]) -> dict:
    """Calculate statistics using functional approach."""
    if not readings:
        return {}
    
    # Using reduce for calculations
    total = reduce(operator.add, readings, 0)
    mean = total / len(readings)
    
    # Using map and reduce for variance
    squared_diffs = map(lambda x: (x - mean) ** 2, readings)
    variance = reduce(operator.add, squared_diffs, 0) / len(readings)
    
    return {
        'count': len(readings),
        'sum': total,
        'mean': mean,
        'variance': variance,
        'std_dev': variance ** 0.5,
        'min': min(readings),
        'max': max(readings)
    }

def demonstrate_functional_programming():
    """Demonstrate functional programming concepts."""
    print("=== Functional Programming Demonstration ===")
    
    # Sample data
    raw_temperature_data = [22.1, 150.0, 23.5, -100.0, 21.8, 24.2, 22.9]
    raw_humidity_data = [65.2, 120.0, 45.8, -10.0, 52.1, 48.7, 51.3]
    
    # Create processing functions
    temp_calibrator = create_calibrator(offset=-0.5, scale=1.02)
    temp_validator = create_filter(min_val=-50, max_val=100)
    temp_normalizer = partial(normalize_reading, min_val=15, max_val=30)
    
    humidity_calibrator = create_calibrator(offset=1.0, scale=0.98)
    humidity_validator = create_filter(min_val=0, max_val=100)
    humidity_normalizer = partial(normalize_reading, min_val=20, max_val=80)
    
    # Process temperature data
    print("\nProcessing temperature data:")
    temp_processed, temp_invalid = process_sensor_data_functional(
        raw_temperature_data,
        temp_calibrator,
        temp_validator,
        temp_normalizer
    )
    
    temp_stats = calculate_statistics_functional(temp_processed)
    print(f"Valid temperature readings: {len(temp_processed)}")
    print(f"Invalid temperature readings: {len(temp_invalid)}")
    print(f"Temperature statistics: {temp_stats}")
    
    # Process humidity data
    print("\nProcessing humidity data:")
    humidity_processed, humidity_invalid = process_sensor_data_functional(
        raw_humidity_data,
        humidity_calibrator,
        humidity_validator,
        humidity_normalizer
    )
    
    humidity_stats = calculate_statistics_functional(humidity_processed)
    print(f"Valid humidity readings: {len(humidity_processed)}")
    print(f"Invalid humidity readings: {len(humidity_invalid)}")
    print(f"Humidity statistics: {humidity_stats}")
    
    # Demonstrate function composition
    print("\nDemonstrating function composition:")
    
    # Compose calibration and normalization
    temp_pipeline = compose_functions(
        temp_normalizer,
        temp_calibrator
    )
    
    sample_reading = 23.0
    calibrated = temp_calibrator(sample_reading)
    normalized = temp_normalizer(calibrated)
    composed_result = temp_pipeline(sample_reading)
    
    print(f"Original reading: {sample_reading}")
    print(f"Step by step: {sample_reading} -> {calibrated} -> {normalized}")
    print(f"Composed function: {sample_reading} -> {composed_result}")
    
    # Demonstrate immutability principle
    print("\nDemonstrating immutability:")
    original_data = [22.1, 23.5, 21.8]
    processed_data = list(map(lambda x: x + 1, original_data))
    
    print(f"Original data (unchanged): {original_data}")
    print(f"Processed data (new list): {processed_data}")

if __name__ == "__main__":
    demonstrate_functional_programming()
```

## Comparing Paradigms

### Choosing the Right Paradigm

```python
# Comparison of paradigms for the same problem

# Problem: Process multiple sensor datasets and generate report

# 1. Procedural approach
def procedural_sensor_processing():
    """Procedural approach to sensor data processing."""
    print("=== Procedural Approach ===")
    
    # Global data structures
    sensor_data = {
        'temperature': [22.1, 23.5, 21.8, 24.2, 22.9],
        'humidity': [65.2, 45.8, 52.1, 48.7, 51.3],
        'pressure': [1013.2, 1015.1, 1010.8, 1012.4, 1014.0]
    }
    
    # Step-by-step processing functions
    def calculate_mean(values):
        return sum(values) / len(values) if values else 0
    
    def calculate_std_dev(values):
        if len(values) < 2:
            return 0
        mean = calculate_mean(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def generate_report(data):
        for sensor_type, readings in data.items():
            mean = calculate_mean(readings)
            std_dev = calculate_std_dev(readings)
            print(f"{sensor_type}: mean={mean:.2f}, std_dev={std_dev:.2f}")
    
    generate_report(sensor_data)

# 2. Object-oriented approach
def oop_sensor_processing():
    """Object-oriented approach to sensor data processing."""
    print("\n=== Object-Oriented Approach ===")
    
    class SensorDataProcessor:
        def __init__(self, sensor_type, readings):
            self.sensor_type = sensor_type
            self.readings = readings
        
        def calculate_mean(self):
            return sum(self.readings) / len(self.readings) if self.readings else 0
        
        def calculate_std_dev(self):
            if len(self.readings) < 2:
                return 0
            mean = self.calculate_mean()
            variance = sum((x - mean) ** 2 for x in self.readings) / len(self.readings)
            return variance ** 0.5
        
        def generate_report(self):
            mean = self.calculate_mean()
            std_dev = self.calculate_std_dev()
            return f"{self.sensor_type}: mean={mean:.2f}, std_dev={std_dev:.2f}"
    
    # Create processor objects
    processors = [
        SensorDataProcessor('temperature', [22.1, 23.5, 21.8, 24.2, 22.9]),
        SensorDataProcessor('humidity', [65.2, 45.8, 52.1, 48.7, 51.3]),
        SensorDataProcessor('pressure', [1013.2, 1015.1, 1010.8, 1012.4, 1014.0])
    ]
    
    # Generate reports
    for processor in processors:
        print(processor.generate_report())

# 3. Functional approach
def functional_sensor_processing():
    """Functional approach to sensor data processing."""
    print("\n=== Functional Approach ===")
    
    from functools import reduce
    import math
    
    # Pure functions
    def calculate_mean(values):
        return reduce(lambda acc, x: acc + x, values, 0) / len(values) if values else 0
    
    def calculate_std_dev(values):
        if len(values) < 2:
            return 0
        mean = calculate_mean(values)
        variance = reduce(lambda acc, x: acc + (x - mean) ** 2, values, 0) / len(values)
        return math.sqrt(variance)
    
    def create_report(sensor_type, readings):
        mean = calculate_mean(readings)
        std_dev = calculate_std_dev(readings)
        return f"{sensor_type}: mean={mean:.2f}, std_dev={std_dev:.2f}"
    
    # Data as immutable structure
    sensor_data = [
        ('temperature', [22.1, 23.5, 21.8, 24.2, 22.9]),
        ('humidity', [65.2, 45.8, 52.1, 48.7, 51.3]),
        ('pressure', [1013.2, 1015.1, 1010.8, 1012.4, 1014.0])
    ]
    
    # Process using map
    reports = list(map(lambda data: create_report(data[0], data[1]), sensor_data))
    
    # Print reports
    for report in reports:
        print(report)

# Demonstrate all approaches
if __name__ == "__main__":
    procedural_sensor_processing()
    oop_sensor_processing()
    functional_sensor_processing()
```

## When to Use Each Paradigm

### Decision Matrix

| Paradigm | Best For | Advantages | Disadvantages |
|----------|----------|------------|---------------|
| **Procedural** | Linear data processing, simple algorithms | Simple, easy to understand, good performance | Can become hard to maintain, global state issues |
| **Object-Oriented** | Complex systems, modeling real-world entities | Encapsulation, reusability, maintainability | Can be over-engineered, performance overhead |
| **Functional** | Data transformations, parallel processing | Immutability, testability, concurrency-safe | Learning curve, potential performance costs |

### Practical Guidelines

```python
# Guidelines for paradigm selection

def paradigm_selection_guide():
    """Guide for selecting appropriate programming paradigm."""
    
    guidelines = {
        "Use Procedural Programming When": [
            "Building simple, linear data processing pipelines",
            "Working with performance-critical algorithms",
            "Creating utility scripts or one-off calculations",
            "Team is new to programming",
            "Problem has clear, sequential steps"
        ],
        
        "Use Object-Oriented Programming When": [
            "Modeling complex systems with multiple entities",
            "Building large, maintainable applications",
            "Need to encapsulate data and behavior together",
            "Multiple developers working on same codebase",
            "Requirements likely to change over time"
        ],
        
        "Use Functional Programming When": [
            "Processing large datasets with transformations",
            "Need high concurrency or parallelism",
            "Working with immutable data structures",
            "Building data processing pipelines",
            "Need predictable, testable code"
        ],
        
        "Hybrid Approaches Work When": [
            "Different parts of system have different needs",
            "Using OOP for structure, FP for data processing",
            "Procedural for algorithms, OOP for organization",
            "Building complex data science applications"
        ]
    }
    
    for category, items in guidelines.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  • {item}")

if __name__ == "__main__":
    paradigm_selection_guide()
```

## Next Steps

Understanding programming paradigms helps you:

1. **Choose the right approach** for different problems
2. **Combine paradigms** effectively in complex applications
3. **Write more maintainable code** by following appropriate patterns
4. **Communicate better** with other developers about design decisions

Continue with:
- **[Tools and Workflow](../tools-workflow/tools-workflow-overview)** - Learn development tools and processes
- **[Python Programming](../python/python-overview)** - Deep dive into Python
- **[C++ Programming](../cpp/cpp-overview)** - Explore C++ for performance-critical tasks

Master these paradigms to become a more effective programmer across different domains and languages!