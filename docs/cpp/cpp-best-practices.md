---
title: C++ Best Practices
---

# C++ Best Practices

## Modern C++ Techniques

### Code Organization and Project Structure

```cpp
// Modern header structure - example: sensor.hpp
#pragma once  // Modern alternative to include guards

#include <vector>
#include <string>
#include <memory>
#include <functional>
#include <optional>

namespace DataProcessing::Sensors {

class ISensor {  // Interface using 'I' prefix
public:
    virtual ~ISensor() = default;
    virtual std::optional<double> readValue() = 0;
    virtual std::string getType() const = 0;
    virtual bool isConnected() const = 0;
};

class TemperatureSensor final : public ISensor {  // 'final' prevents inheritance
private:
    std::string m_deviceId;  // Member prefix convention
    mutable std::optional<double> m_cachedValue;  // Mutable for caching
    
public:
    explicit TemperatureSensor(std::string deviceId);  // Explicit constructor
    
    // Rule of Five - explicitly defaulted/deleted
    ~TemperatureSensor() override = default;
    TemperatureSensor(const TemperatureSensor&) = delete;
    TemperatureSensor& operator=(const TemperatureSensor&) = delete;
    TemperatureSensor(TemperatureSensor&&) = default;
    TemperatureSensor& operator=(TemperatureSensor&&) = default;
    
    // Override specifier for virtual functions
    std::optional<double> readValue() override;
    std::string getType() const override;
    bool isConnected() const override;
    
    // Modern C++ features
    [[nodiscard]] double getLastReading() const;  // Attribute
    void setCallback(std::function<void(double)> callback);
};

}  // namespace DataProcessing::Sensors
```

### Modern C++ Features (C++11 and beyond)

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>
#include <string>
#include <optional>
#include <variant>
#include <any>

namespace ModernCpp {

// Scoped enums (C++11)
enum class SensorStatus {
    DISCONNECTED,
    CONNECTED,
    ERROR,
    CALIBRATING
};

// Alias declarations (C++11)
using SensorPtr = std::unique_ptr<class Sensor>;
using SensorCollection = std::vector<SensorPtr>;
using ProcessingFunction = std::function<double(double)>;

class DataProcessor {
private:
    std::vector<double> m_data;
    
public:
    // Range-based for loops (C++11)
    void processData() {
        std::cout << "Processing data using range-based for:" << std::endl;
        for (const auto& value : m_data) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
    
    // Auto keyword (C++11)
    auto calculateStatistics() {
        struct Statistics {
            double mean;
            double min;
            double max;
        };
        
        if (m_data.empty()) {
            return Statistics{0.0, 0.0, 0.0};
        }
        
        auto [min_it, max_it] = std::minmax_element(m_data.begin(), m_data.end()); // Structured bindings (C++17)
        
        double sum = 0.0;
        for (const auto& value : m_data) {
            sum += value;
        }
        
        return Statistics{sum / m_data.size(), *min_it, *max_it};
    }
    
    // Lambda expressions (C++11)
    void applyFilter(double threshold) {
        std::cout << "Applying filter with lambda:" << std::endl;
        
        // Capture by reference [&], by value [=], or mixed
        auto isValid = [threshold](double value) {
            return value >= threshold;
        };
        
        auto validCount = std::count_if(m_data.begin(), m_data.end(), isValid);
        std::cout << "Valid readings: " << validCount << "/" << m_data.size() << std::endl;
        
        // Remove invalid readings
        m_data.erase(
            std::remove_if(m_data.begin(), m_data.end(), 
                          [threshold](double value) { return value < threshold; }),
            m_data.end()
        );
    }
    
    // Variadic templates (C++11)
    template<typename... Args>
    void addReadings(Args... values) {
        // Fold expression (C++17)
        (m_data.push_back(values), ...);
    }
    
    // Perfect forwarding (C++11)
    template<typename Func>
    auto applyFunction(Func&& func) -> decltype(func(m_data[0])) {
        if (m_data.empty()) {
            throw std::runtime_error("No data to process");
        }
        return std::forward<Func>(func)(m_data[0]);
    }
    
    // Optional return (C++17)
    std::optional<double> getSafeValue(size_t index) const {
        if (index < m_data.size()) {
            return m_data[index];
        }
        return std::nullopt;
    }
    
    // Variant for polymorphic data (C++17)
    using SensorReading = std::variant<double, int, std::string>;
    
    void processMixedReading(const SensorReading& reading) {
        std::visit([](const auto& value) {
            using T = std::decay_t<decltype(value)>;
            if constexpr (std::is_same_v<T, double>) {
                std::cout << "Double reading: " << value << std::endl;
            } else if constexpr (std::is_same_v<T, int>) {
                std::cout << "Integer reading: " << value << std::endl;
            } else if constexpr (std::is_same_v<T, std::string>) {
                std::cout << "String reading: " << value << std::endl;
            }
        }, reading);
    }
    
    void printData() const {
        std::cout << "Data: ";
        for (const auto& value : m_data) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
};

void demonstrateModernFeatures() {
    std::cout << "=== Modern C++ Features Demo ===" << std::endl;
    
    DataProcessor processor;
    
    // Variadic template usage
    processor.addReadings(22.5, 23.1, 21.8, 24.2, 22.9);
    processor.printData();
    
    // Auto and structured bindings
    auto stats = processor.calculateStatistics();
    std::cout << "Statistics - Mean: " << stats.mean 
              << ", Min: " << stats.min 
              << ", Max: " << stats.max << std::endl;
    
    // Lambda and algorithms
    processor.applyFilter(22.0);
    processor.printData();
    
    // Optional usage
    if (auto value = processor.getSafeValue(0)) {
        std::cout << "First value: " << *value << std::endl;
    }
    
    if (auto value = processor.getSafeValue(100)) {
        std::cout << "100th value: " << *value << std::endl;
    } else {
        std::cout << "100th value doesn't exist" << std::endl;
    }
    
    // Variant usage
    std::vector<DataProcessor::SensorReading> readings = {
        25.5,
        42,
        std::string("ERROR")
    };
    
    for (const auto& reading : readings) {
        processor.processMixedReading(reading);
    }
    
    // Perfect forwarding
    auto doubleValue = processor.applyFunction([](double x) { return x * 2; });
    std::cout << "Doubled first value: " << doubleValue << std::endl;
}

}  // namespace ModernCpp
```

### Error Handling Best Practices

```cpp
#include <iostream>
#include <stdexcept>
#include <system_error>
#include <optional>
#include <expected>  // C++23 (or use alternative implementation)

namespace ErrorHandling {

// Custom exception hierarchy
class SensorException : public std::runtime_error {
public:
    explicit SensorException(const std::string& message) 
        : std::runtime_error("Sensor Error: " + message) {}
};

class ConnectionException : public SensorException {
public:
    explicit ConnectionException(const std::string& device) 
        : SensorException("Failed to connect to device: " + device) {}
};

class CalibrationException : public SensorException {
public:
    explicit CalibrationException(const std::string& reason) 
        : SensorException("Calibration failed: " + reason) {}
};

// Error codes enum
enum class SensorError {
    SUCCESS = 0,
    CONNECTION_FAILED,
    CALIBRATION_FAILED,
    INVALID_DATA,
    TIMEOUT
};

// Error handling with optional
class SafeSensor {
private:
    std::string m_deviceId;
    bool m_connected;
    
public:
    explicit SafeSensor(std::string deviceId) 
        : m_deviceId(std::move(deviceId)), m_connected(false) {}
    
    std::optional<bool> connect() noexcept {
        try {
            // Simulate connection logic
            if (m_deviceId.empty()) {
                return std::nullopt;
            }
            
            m_connected = true;
            return true;
        } catch (...) {
            return std::nullopt;
        }
    }
    
    std::optional<double> readTemperature() noexcept {
        if (!m_connected) {
            return std::nullopt;
        }
        
        try {
            // Simulate reading
            double value = 22.5 + (rand() % 100) / 10.0;
            
            if (value < -50 || value > 100) {
                return std::nullopt;  // Invalid reading
            }
            
            return value;
        } catch (...) {
            return std::nullopt;
        }
    }
    
    // Exception-based error handling
    void connectWithExceptions() {
        if (m_deviceId.empty()) {
            throw std::invalid_argument("Device ID cannot be empty");
        }
        
        // Simulate connection failure
        if (m_deviceId == "INVALID") {
            throw ConnectionException(m_deviceId);
        }
        
        m_connected = true;
    }
    
    double readTemperatureWithExceptions() {
        if (!m_connected) {
            throw std::runtime_error("Sensor not connected");
        }
        
        double value = 22.5 + (rand() % 100) / 10.0;
        
        if (value < -50 || value > 100) {
            throw std::out_of_range("Temperature reading out of valid range: " + std::to_string(value));
        }
        
        return value;
    }
    
    bool isConnected() const noexcept { return m_connected; }
    const std::string& getDeviceId() const noexcept { return m_deviceId; }
};

// Result type pattern (C++23 std::expected alternative)
template<typename T, typename E>
class Result {
private:
    bool m_hasValue;
    union {
        T m_value;
        E m_error;
    };
    
public:
    Result(T value) : m_hasValue(true), m_value(std::move(value)) {}
    Result(E error) : m_hasValue(false), m_error(std::move(error)) {}
    
    ~Result() {
        if (m_hasValue) {
            m_value.~T();
        } else {
            m_error.~E();
        }
    }
    
    bool hasValue() const { return m_hasValue; }
    const T& value() const { 
        if (!m_hasValue) throw std::runtime_error("Result contains error");
        return m_value; 
    }
    const E& error() const { 
        if (m_hasValue) throw std::runtime_error("Result contains value");
        return m_error; 
    }
    
    explicit operator bool() const { return m_hasValue; }
};

class ResultBasedSensor {
private:
    std::string m_deviceId;
    bool m_connected;
    
public:
    explicit ResultBasedSensor(std::string deviceId) 
        : m_deviceId(std::move(deviceId)), m_connected(false) {}
    
    Result<bool, SensorError> connect() {
        if (m_deviceId.empty()) {
            return SensorError::CONNECTION_FAILED;
        }
        
        m_connected = true;
        return true;
    }
    
    Result<double, SensorError> readTemperature() {
        if (!m_connected) {
            return SensorError::CONNECTION_FAILED;
        }
        
        double value = 22.5 + (rand() % 100) / 10.0;
        
        if (value < -50 || value > 100) {
            return SensorError::INVALID_DATA;
        }
        
        return value;
    }
};

void demonstrateErrorHandling() {
    std::cout << "=== Error Handling Best Practices ===" << std::endl;
    
    // Optional-based error handling
    std::cout << "\n1. Optional-based error handling:" << std::endl;
    SafeSensor optionalSensor("TEMP-01");
    
    if (auto connected = optionalSensor.connect()) {
        std::cout << "Connected successfully" << std::endl;
        
        if (auto temperature = optionalSensor.readTemperature()) {
            std::cout << "Temperature: " << *temperature << "°C" << std::endl;
        } else {
            std::cout << "Failed to read temperature" << std::endl;
        }
    } else {
        std::cout << "Failed to connect" << std::endl;
    }
    
    // Exception-based error handling
    std::cout << "\n2. Exception-based error handling:" << std::endl;
    try {
        SafeSensor exceptionSensor("TEMP-02");
        exceptionSensor.connectWithExceptions();
        
        for (int i = 0; i < 3; ++i) {
            try {
                double temp = exceptionSensor.readTemperatureWithExceptions();
                std::cout << "Reading " << i << ": " << temp << "°C" << std::endl;
            } catch (const std::out_of_range& e) {
                std::cout << "Invalid reading: " << e.what() << std::endl;
            }
        }
    } catch (const SensorException& e) {
        std::cout << "Sensor error: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "General error: " << e.what() << std::endl;
    }
    
    // Result-based error handling
    std::cout << "\n3. Result-based error handling:" << std::endl;
    ResultBasedSensor resultSensor("TEMP-03");
    
    auto connectResult = resultSensor.connect();
    if (connectResult) {
        std::cout << "Connected successfully" << std::endl;
        
        for (int i = 0; i < 3; ++i) {
            auto tempResult = resultSensor.readTemperature();
            if (tempResult) {
                std::cout << "Reading " << i << ": " << tempResult.value() << "°C" << std::endl;
            } else {
                std::cout << "Failed to read temperature, error code: " 
                          << static_cast<int>(tempResult.error()) << std::endl;
            }
        }
    } else {
        std::cout << "Failed to connect, error code: " 
                  << static_cast<int>(connectResult.error()) << std::endl;
    }
}

}  // namespace ErrorHandling
```

### Performance Optimization

```cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>
#include <memory>
#include <string>

namespace Performance {

class OptimizedDataProcessor {
private:
    std::vector<double> m_data;
    
public:
    // Reserve capacity to avoid reallocations
    explicit OptimizedDataProcessor(size_t expectedSize = 1000) {
        m_data.reserve(expectedSize);
    }
    
    // Move semantics for efficient transfers
    void addData(std::vector<double>&& data) {
        m_data = std::move(data);  // No copying
    }
    
    void addData(const std::vector<double>& data) {
        m_data.reserve(m_data.size() + data.size());
        m_data.insert(m_data.end(), data.begin(), data.end());
    }
    
    // Emplace for in-place construction
    template<typename... Args>
    void emplaceReading(Args&&... args) {
        m_data.emplace_back(std::forward<Args>(args)...);
    }
    
    // Const correctness for read operations
    double calculateMean() const {
        if (m_data.empty()) return 0.0;
        
        double sum = 0.0;
        for (const auto& value : m_data) {
            sum += value;
        }
        return sum / m_data.size();
    }
    
    // Pass by const reference for large objects
    void processLargeData(const std::vector<std::vector<double>>& matrix) const {
        std::cout << "Processing matrix with " << matrix.size() << " rows" << std::endl;
        // Process without copying
    }
    
    // Return by value for small objects, const reference for large
    const std::vector<double>& getData() const & {  // Lvalue reference qualifier
        return m_data;
    }
    
    std::vector<double>&& getData() && {  // Rvalue reference qualifier
        return std::move(m_data);
    }
    
    // Cache expensive calculations
    mutable std::optional<double> m_cachedStandardDeviation;
    
    double getStandardDeviation() const {
        if (!m_cachedStandardDeviation) {
            double mean = calculateMean();
            double sumSquaredDiffs = 0.0;
            
            for (const auto& value : m_data) {
                double diff = value - mean;
                sumSquaredDiffs += diff * diff;
            }
            
            m_cachedStandardDeviation = std::sqrt(sumSquaredDiffs / m_data.size());
        }
        
        return *m_cachedStandardDeviation;
    }
    
    void invalidateCache() {
        m_cachedStandardDeviation.reset();
    }
    
    // Memory pool for frequent allocations
    class MemoryPool {
    private:
        std::vector<std::unique_ptr<double[]>> m_blocks;
        size_t m_blockSize;
        size_t m_currentBlock;
        size_t m_currentIndex;
        
    public:
        explicit MemoryPool(size_t blockSize = 1000) 
            : m_blockSize(blockSize), m_currentBlock(0), m_currentIndex(0) {
            m_blocks.push_back(std::make_unique<double[]>(blockSize));
        }
        
        double* allocate(size_t count) {
            if (m_currentIndex + count > m_blockSize) {
                // Need new block
                m_blocks.push_back(std::make_unique<double[]>(m_blockSize));
                m_currentBlock++;
                m_currentIndex = 0;
            }
            
            double* ptr = &m_blocks[m_currentBlock][m_currentIndex];
            m_currentIndex += count;
            return ptr;
        }
        
        void reset() {
            m_currentBlock = 0;
            m_currentIndex = 0;
        }
    };
    
private:
    static MemoryPool s_pool;
    
public:
    static double* allocateTemporaryArray(size_t size) {
        return s_pool.allocate(size);
    }
    
    static void resetPool() {
        s_pool.reset();
    }
};

// Static member definition
OptimizedDataProcessor::MemoryPool OptimizedDataProcessor::s_pool;

// Benchmark helper
class Benchmark {
private:
    std::chrono::high_resolution_clock::time_point m_start;
    std::string m_name;
    
public:
    explicit Benchmark(std::string name) : m_name(std::move(name)) {
        m_start = std::chrono::high_resolution_clock::now();
    }
    
    ~Benchmark() {
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - m_start);
        std::cout << m_name << " took: " << duration.count() << " microseconds" << std::endl;
    }
};

void demonstratePerformanceOptimizations() {
    std::cout << "=== Performance Optimization Demo ===" << std::endl;
    
    const size_t dataSize = 100000;
    
    // Test 1: Reserve vs no reserve
    {
        Benchmark bench("Vector without reserve");
        std::vector<double> data;
        for (size_t i = 0; i < dataSize; ++i) {
            data.push_back(i * 0.1);
        }
    }
    
    {
        Benchmark bench("Vector with reserve");
        std::vector<double> data;
        data.reserve(dataSize);
        for (size_t i = 0; i < dataSize; ++i) {
            data.push_back(i * 0.1);
        }
    }
    
    // Test 2: Copy vs move
    std::vector<double> sourceData(dataSize);
    std::generate(sourceData.begin(), sourceData.end(), []() {
        return rand() % 1000 / 10.0;
    });
    
    {
        Benchmark bench("Data copy");
        OptimizedDataProcessor processor1;
        processor1.addData(sourceData);  // Copy
    }
    
    {
        Benchmark bench("Data move");
        OptimizedDataProcessor processor2;
        std::vector<double> moveData = sourceData;  // Copy for test
        processor2.addData(std::move(moveData));    // Move
    }
    
    // Test 3: Caching expensive calculations
    OptimizedDataProcessor processor(dataSize);
    std::vector<double> testData(dataSize);
    std::generate(testData.begin(), testData.end(), []() {
        return rand() % 1000 / 10.0;
    });
    processor.addData(std::move(testData));
    
    {
        Benchmark bench("First std dev calculation (no cache)");
        double stdDev = processor.getStandardDeviation();
        std::cout << "Standard deviation: " << stdDev << std::endl;
    }
    
    {
        Benchmark bench("Second std dev calculation (cached)");
        double stdDev = processor.getStandardDeviation();
        std::cout << "Standard deviation: " << stdDev << std::endl;
    }
    
    // Test 4: Memory pool usage
    {
        Benchmark bench("Regular allocation");
        std::vector<double*> arrays;
        for (int i = 0; i < 1000; ++i) {
            arrays.push_back(new double[100]);
        }
        for (auto* ptr : arrays) {
            delete[] ptr;
        }
    }
    
    {
        Benchmark bench("Memory pool allocation");
        std::vector<double*> arrays;
        for (int i = 0; i < 1000; ++i) {
            arrays.push_back(OptimizedDataProcessor::allocateTemporaryArray(100));
        }
        OptimizedDataProcessor::resetPool();
    }
}

}  // namespace Performance
```

### Design Patterns in C++

```cpp
#include <iostream>
#include <memory>
#include <vector>
#include <unordered_map>
#include <functional>

namespace DesignPatterns {

// Singleton Pattern (thread-safe)
class DataLogger {
private:
    static std::unique_ptr<DataLogger> s_instance;
    static std::once_flag s_initFlag;
    
    DataLogger() = default;
    
public:
    static DataLogger& getInstance() {
        std::call_once(s_initFlag, []() {
            s_instance = std::make_unique<DataLogger>();
        });
        return *s_instance;
    }
    
    void log(const std::string& message) {
        std::cout << "[LOG] " << message << std::endl;
    }
    
    // Delete copy/move operations
    DataLogger(const DataLogger&) = delete;
    DataLogger& operator=(const DataLogger&) = delete;
    DataLogger(DataLogger&&) = delete;
    DataLogger& operator=(DataLogger&&) = delete;
};

// Static member definitions
std::unique_ptr<DataLogger> DataLogger::s_instance;
std::once_flag DataLogger::s_initFlag;

// Factory Pattern
class ISensor {
public:
    virtual ~ISensor() = default;
    virtual double readValue() = 0;
    virtual std::string getType() const = 0;
};

class TemperatureSensor : public ISensor {
public:
    double readValue() override {
        return 22.5 + (rand() % 100) / 10.0;
    }
    
    std::string getType() const override {
        return "Temperature";
    }
};

class PressureSensor : public ISensor {
public:
    double readValue() override {
        return 1013.25 + (rand() % 100) / 10.0;
    }
    
    std::string getType() const override {
        return "Pressure";
    }
};

class SensorFactory {
public:
    enum class SensorType {
        TEMPERATURE,
        PRESSURE
    };
    
    static std::unique_ptr<ISensor> createSensor(SensorType type) {
        switch (type) {
            case SensorType::TEMPERATURE:
                return std::make_unique<TemperatureSensor>();
            case SensorType::PRESSURE:
                return std::make_unique<PressureSensor>();
            default:
                throw std::invalid_argument("Unknown sensor type");
        }
    }
};

// Observer Pattern
class IObserver {
public:
    virtual ~IObserver() = default;
    virtual void onSensorDataChanged(const std::string& sensorId, double value) = 0;
};

class Subject {
private:
    std::vector<std::weak_ptr<IObserver>> m_observers;
    
public:
    void addObserver(std::shared_ptr<IObserver> observer) {
        m_observers.push_back(observer);
    }
    
    void removeObserver(std::shared_ptr<IObserver> observer) {
        m_observers.erase(
            std::remove_if(m_observers.begin(), m_observers.end(),
                          [&observer](const std::weak_ptr<IObserver>& weak) {
                              return weak.lock() == observer;
                          }),
            m_observers.end()
        );
    }
    
protected:
    void notifyObservers(const std::string& sensorId, double value) {
        // Clean up expired weak_ptrs and notify valid observers
        auto it = m_observers.begin();
        while (it != m_observers.end()) {
            if (auto observer = it->lock()) {
                observer->onSensorDataChanged(sensorId, value);
                ++it;
            } else {
                it = m_observers.erase(it);
            }
        }
    }
};

class SmartSensor : public Subject {
private:
    std::string m_id;
    std::unique_ptr<ISensor> m_sensor;
    
public:
    SmartSensor(std::string id, std::unique_ptr<ISensor> sensor)
        : m_id(std::move(id)), m_sensor(std::move(sensor)) {}
    
    void takeReading() {
        double value = m_sensor->readValue();
        DataLogger::getInstance().log("Sensor " + m_id + " reading: " + std::to_string(value));
        notifyObservers(m_id, value);
    }
    
    const std::string& getId() const { return m_id; }
    std::string getType() const { return m_sensor->getType(); }
};

class DataDisplay : public IObserver {
private:
    std::string m_name;
    
public:
    explicit DataDisplay(std::string name) : m_name(std::move(name)) {}
    
    void onSensorDataChanged(const std::string& sensorId, double value) override {
        std::cout << "[" << m_name << "] Sensor " << sensorId 
                  << " reported: " << value << std::endl;
    }
};

class DataArchiver : public IObserver {
private:
    std::unordered_map<std::string, std::vector<double>> m_archive;
    
public:
    void onSensorDataChanged(const std::string& sensorId, double value) override {
        m_archive[sensorId].push_back(value);
        std::cout << "[Archiver] Stored reading for " << sensorId 
                  << " (total: " << m_archive[sensorId].size() << ")" << std::endl;
    }
    
    void printArchive() const {
        for (const auto& [sensorId, readings] : m_archive) {
            std::cout << "Sensor " << sensorId << " has " << readings.size() << " readings" << std::endl;
        }
    }
};

// Strategy Pattern
class IProcessingStrategy {
public:
    virtual ~IProcessingStrategy() = default;
    virtual double process(const std::vector<double>& data) = 0;
    virtual std::string getName() const = 0;
};

class MeanStrategy : public IProcessingStrategy {
public:
    double process(const std::vector<double>& data) override {
        if (data.empty()) return 0.0;
        
        double sum = 0.0;
        for (const auto& value : data) {
            sum += value;
        }
        return sum / data.size();
    }
    
    std::string getName() const override { return "Mean"; }
};

class MedianStrategy : public IProcessingStrategy {
public:
    double process(const std::vector<double>& data) override {
        if (data.empty()) return 0.0;
        
        std::vector<double> sorted = data;
        std::sort(sorted.begin(), sorted.end());
        
        size_t n = sorted.size();
        if (n % 2 == 0) {
            return (sorted[n/2 - 1] + sorted[n/2]) / 2.0;
        } else {
            return sorted[n/2];
        }
    }
    
    std::string getName() const override { return "Median"; }
};

class DataAnalyzer {
private:
    std::unique_ptr<IProcessingStrategy> m_strategy;
    
public:
    void setStrategy(std::unique_ptr<IProcessingStrategy> strategy) {
        m_strategy = std::move(strategy);
    }
    
    double analyze(const std::vector<double>& data) {
        if (!m_strategy) {
            throw std::runtime_error("No processing strategy set");
        }
        
        double result = m_strategy->process(data);
        std::cout << m_strategy->getName() << " result: " << result << std::endl;
        return result;
    }
};

void demonstrateDesignPatterns() {
    std::cout << "=== Design Patterns Demo ===" << std::endl;
    
    // Singleton Pattern
    std::cout << "\n1. Singleton Pattern:" << std::endl;
    DataLogger::getInstance().log("Application started");
    
    // Factory Pattern
    std::cout << "\n2. Factory Pattern:" << std::endl;
    auto tempSensor = SensorFactory::createSensor(SensorFactory::SensorType::TEMPERATURE);
    auto pressureSensor = SensorFactory::createSensor(SensorFactory::SensorType::PRESSURE);
    
    std::cout << "Created " << tempSensor->getType() << " sensor" << std::endl;
    std::cout << "Created " << pressureSensor->getType() << " sensor" << std::endl;
    
    // Observer Pattern
    std::cout << "\n3. Observer Pattern:" << std::endl;
    SmartSensor smartTemp("TEMP-01", std::move(tempSensor));
    SmartSensor smartPressure("PRESS-01", std::move(pressureSensor));
    
    auto display = std::make_shared<DataDisplay>("Dashboard");
    auto archiver = std::make_shared<DataArchiver>();
    
    smartTemp.addObserver(display);
    smartTemp.addObserver(archiver);
    smartPressure.addObserver(display);
    smartPressure.addObserver(archiver);
    
    // Take some readings
    for (int i = 0; i < 3; ++i) {
        smartTemp.takeReading();
        smartPressure.takeReading();
    }
    
    archiver->printArchive();
    
    // Strategy Pattern
    std::cout << "\n4. Strategy Pattern:" << std::endl;
    std::vector<double> testData = {22.5, 23.1, 21.8, 24.2, 22.9, 23.5, 22.3};
    
    DataAnalyzer analyzer;
    
    analyzer.setStrategy(std::make_unique<MeanStrategy>());
    analyzer.analyze(testData);
    
    analyzer.setStrategy(std::make_unique<MedianStrategy>());
    analyzer.analyze(testData);
}

}  // namespace DesignPatterns
```

## Next Steps

You now have a comprehensive understanding of C++ best practices including:

- Modern C++ features (C++11/14/17/20)
- Error handling strategies
- Performance optimization techniques
- Common design patterns

Continue exploring:

- **[Programming Fundamentals](../programming/paradigms)** - Compare C++ with other programming approaches
- **[Python Overview](../python/python-overview)** - See how Python handles similar concepts
- **Advanced Topics:** STL algorithms, concurrency, template metaprogramming

These best practices will help you write maintainable, efficient, and robust C++ code for data processing applications!