---
title: C++ Object-Oriented Programming
---

# C++ Object-Oriented Programming

## Classes and Objects

Object-oriented programming in C++ allows you to model real-world entities as classes with data (attributes) and behaviors (methods).

### Basic Class Structure

```cpp
#include <iostream>
#include <vector>
#include <string>

class TemperatureSensor {
private:
    // Private data members (encapsulation)
    std::string sensorId;
    std::vector<double> readings;
    double calibrationOffset;
    bool isActive;
    
public:
    // Constructor
    TemperatureSensor(const std::string& id, double offset = 0.0) 
        : sensorId(id), calibrationOffset(offset), isActive(true) {
        std::cout << "Created sensor: " << sensorId << std::endl;
        readings.reserve(100);  // Pre-allocate space for efficiency
    }
    
    // Destructor
    ~TemperatureSensor() {
        std::cout << "Destroyed sensor: " << sensorId << std::endl;
    }
    
    // Public methods
    void addReading(double temperature) {
        if (isActive) {
            readings.push_back(temperature + calibrationOffset);
        }
    }
    
    double getAverageTemperature() const {
        if (readings.empty()) {
            return 0.0;
        }
        
        double sum = 0.0;
        for (const auto& reading : readings) {
            sum += reading;
        }
        return sum / readings.size();
    }
    
    size_t getReadingCount() const {
        return readings.size();
    }
    
    std::string getId() const {
        return sensorId;
    }
    
    void setActive(bool active) {
        isActive = active;
        std::cout << "Sensor " << sensorId << " is now " 
                  << (active ? "active" : "inactive") << std::endl;
    }
    
    bool getActive() const {
        return isActive;
    }
    
    void printReport() const {
        std::cout << "=== Sensor Report ===" << std::endl;
        std::cout << "ID: " << sensorId << std::endl;
        std::cout << "Status: " << (isActive ? "Active" : "Inactive") << std::endl;
        std::cout << "Readings: " << readings.size() << std::endl;
        std::cout << "Average: " << getAverageTemperature() << "°C" << std::endl;
        std::cout << "Calibration offset: " << calibrationOffset << "°C" << std::endl;
        
        if (!readings.empty()) {
            double minTemp = readings[0];
            double maxTemp = readings[0];
            for (const auto& reading : readings) {
                if (reading < minTemp) minTemp = reading;
                if (reading > maxTemp) maxTemp = reading;
            }
            std::cout << "Range: " << minTemp << "°C to " << maxTemp << "°C" << std::endl;
        }
    }
};

void demonstrateBasicClass() {
    // Create sensor objects
    TemperatureSensor outdoor("OUTDOOR-01", -0.5);
    TemperatureSensor indoor("INDOOR-01");
    
    // Add readings
    outdoor.addReading(15.2);
    outdoor.addReading(16.8);
    outdoor.addReading(14.9);
    outdoor.addReading(17.1);
    
    indoor.addReading(22.1);
    indoor.addReading(21.8);
    indoor.addReading(22.5);
    indoor.addReading(22.0);
    
    // Test deactivation
    outdoor.setActive(false);
    outdoor.addReading(20.0);  // This won't be recorded
    outdoor.setActive(true);
    
    // Print reports
    outdoor.printReport();
    std::cout << std::endl;
    indoor.printReport();
}
```

### Constructor and Destructor Variants

```cpp
#include <iostream>
#include <string>
#include <memory>

class DataLogger {
private:
    std::string filename;
    size_t maxEntries;
    size_t currentEntries;
    
public:
    // Default constructor
    DataLogger() : filename("default.log"), maxEntries(1000), currentEntries(0) {
        std::cout << "Default constructor called" << std::endl;
    }
    
    // Parameterized constructor
    DataLogger(const std::string& file, size_t max = 1000) 
        : filename(file), maxEntries(max), currentEntries(0) {
        std::cout << "Parameterized constructor called for " << filename << std::endl;
    }
    
    // Copy constructor
    DataLogger(const DataLogger& other) 
        : filename(other.filename + "_copy"), 
          maxEntries(other.maxEntries), 
          currentEntries(0) {
        std::cout << "Copy constructor called for " << filename << std::endl;
    }
    
    // Move constructor (C++11)
    DataLogger(DataLogger&& other) noexcept
        : filename(std::move(other.filename)),
          maxEntries(other.maxEntries),
          currentEntries(other.currentEntries) {
        std::cout << "Move constructor called" << std::endl;
        other.currentEntries = 0;
    }
    
    // Copy assignment operator
    DataLogger& operator=(const DataLogger& other) {
        if (this != &other) {
            filename = other.filename + "_assigned";
            maxEntries = other.maxEntries;
            currentEntries = 0;
            std::cout << "Copy assignment called for " << filename << std::endl;
        }
        return *this;
    }
    
    // Move assignment operator (C++11)
    DataLogger& operator=(DataLogger&& other) noexcept {
        if (this != &other) {
            filename = std::move(other.filename);
            maxEntries = other.maxEntries;
            currentEntries = other.currentEntries;
            other.currentEntries = 0;
            std::cout << "Move assignment called" << std::endl;
        }
        return *this;
    }
    
    // Destructor
    ~DataLogger() {
        std::cout << "Destructor called for " << filename << std::endl;
    }
    
    void logEntry(const std::string& message) {
        if (currentEntries < maxEntries) {
            std::cout << "[" << filename << "] " << message << std::endl;
            currentEntries++;
        }
    }
    
    std::string getFilename() const { return filename; }
    size_t getCurrentEntries() const { return currentEntries; }
};

void demonstrateConstructorsAndDestructors() {
    std::cout << "=== Constructor/Destructor Demo ===" << std::endl;
    
    // Default constructor
    DataLogger logger1;
    logger1.logEntry("Default logger message");
    
    // Parameterized constructor
    DataLogger logger2("sensor_data.log", 500);
    logger2.logEntry("Parameterized logger message");
    
    // Copy constructor
    DataLogger logger3 = logger2;  // Copy constructor
    logger3.logEntry("Copied logger message");
    
    // Copy assignment
    DataLogger logger4;
    logger4 = logger2;  // Copy assignment
    logger4.logEntry("Assigned logger message");
    
    // Move operations (typically used with temporary objects)
    DataLogger logger5 = std::move(logger2);  // Move constructor
    logger5.logEntry("Moved logger message");
    
    std::cout << "Original logger filename after move: " << logger2.getFilename() << std::endl;
}
```

## Inheritance

### Basic Inheritance

```cpp
#include <iostream>
#include <vector>
#include <memory>

// Base class
class Sensor {
protected:  // Accessible to derived classes
    std::string sensorId;
    std::vector<double> readings;
    bool isCalibrated;
    
public:
    Sensor(const std::string& id) : sensorId(id), isCalibrated(false) {
        std::cout << "Base Sensor constructor: " << sensorId << std::endl;
    }
    
    virtual ~Sensor() {  // Virtual destructor for proper cleanup
        std::cout << "Base Sensor destructor: " << sensorId << std::endl;
    }
    
    virtual void addReading(double value) {
        readings.push_back(value);
    }
    
    virtual double getAverage() const {
        if (readings.empty()) return 0.0;
        
        double sum = 0.0;
        for (const auto& reading : readings) {
            sum += reading;
        }
        return sum / readings.size();
    }
    
    // Pure virtual functions (abstract methods)
    virtual std::string getUnit() const = 0;
    virtual std::string getType() const = 0;
    virtual void calibrate() = 0;
    
    virtual void printReport() const {
        std::cout << "Sensor: " << sensorId << " (" << getType() << ")" << std::endl;
        std::cout << "Readings: " << readings.size() << std::endl;
        std::cout << "Average: " << getAverage() << " " << getUnit() << std::endl;
        std::cout << "Calibrated: " << (isCalibrated ? "Yes" : "No") << std::endl;
    }
    
    std::string getId() const { return sensorId; }
    bool getCalibrated() const { return isCalibrated; }
};

// Derived class 1
class TemperatureSensor : public Sensor {
private:
    double calibrationOffset;
    double minTemp, maxTemp;
    
public:
    TemperatureSensor(const std::string& id, double offset = 0.0) 
        : Sensor(id), calibrationOffset(offset), minTemp(-40.0), maxTemp(85.0) {
        std::cout << "TemperatureSensor constructor: " << sensorId << std::endl;
    }
    
    ~TemperatureSensor() override {
        std::cout << "TemperatureSensor destructor: " << sensorId << std::endl;
    }
    
    void addReading(double temperature) override {
        // Apply calibration and validate range
        double calibratedTemp = temperature + calibrationOffset;
        
        if (calibratedTemp >= minTemp && calibratedTemp <= maxTemp) {
            Sensor::addReading(calibratedTemp);
        } else {
            std::cout << "Warning: Temperature " << calibratedTemp 
                      << "°C out of range [" << minTemp << ", " << maxTemp << "]" << std::endl;
        }
    }
    
    std::string getUnit() const override {
        return "°C";
    }
    
    std::string getType() const override {
        return "Temperature";
    }
    
    void calibrate() override {
        // Simulate calibration process
        std::cout << "Calibrating temperature sensor " << sensorId << "..." << std::endl;
        calibrationOffset = 0.2;  // Adjust based on calibration
        isCalibrated = true;
    }
    
    void setTemperatureRange(double min, double max) {
        minTemp = min;
        maxTemp = max;
        std::cout << "Temperature range set to [" << min << ", " << max << "]°C" << std::endl;
    }
};

// Derived class 2
class PressureSensor : public Sensor {
private:
    double conversionFactor;
    std::string pressureUnit;
    
public:
    PressureSensor(const std::string& id, const std::string& unit = "Pa", double factor = 1.0) 
        : Sensor(id), conversionFactor(factor), pressureUnit(unit) {
        std::cout << "PressureSensor constructor: " << sensorId << std::endl;
    }
    
    ~PressureSensor() override {
        std::cout << "PressureSensor destructor: " << sensorId << std::endl;
    }
    
    void addReading(double pressure) override {
        double convertedPressure = pressure * conversionFactor;
        Sensor::addReading(convertedPressure);
    }
    
    std::string getUnit() const override {
        return pressureUnit;
    }
    
    std::string getType() const override {
        return "Pressure";
    }
    
    void calibrate() override {
        std::cout << "Calibrating pressure sensor " << sensorId << "..." << std::endl;
        // Simulate atmospheric pressure calibration
        conversionFactor = 1.013;
        isCalibrated = true;
    }
    
    void setUnit(const std::string& unit, double factor) {
        pressureUnit = unit;
        conversionFactor = factor;
        std::cout << "Pressure unit changed to " << unit 
                  << " with factor " << factor << std::endl;
    }
};

void demonstrateInheritance() {
    std::cout << "=== Inheritance Demo ===" << std::endl;
    
    // Create sensors using polymorphism
    std::vector<std::unique_ptr<Sensor>> sensors;
    
    sensors.push_back(std::make_unique<TemperatureSensor>("TEMP-01", -0.2));
    sensors.push_back(std::make_unique<PressureSensor>("PRESS-01", "hPa", 0.01));
    sensors.push_back(std::make_unique<TemperatureSensor>("TEMP-02"));
    
    // Add readings
    sensors[0]->addReading(22.5);
    sensors[0]->addReading(23.1);
    sensors[0]->addReading(22.8);
    
    sensors[1]->addReading(101325);  // Pa
    sensors[1]->addReading(101280);
    sensors[1]->addReading(101345);
    
    sensors[2]->addReading(18.2);
    sensors[2]->addReading(18.8);
    
    // Calibrate all sensors
    std::cout << "\nCalibrating all sensors:" << std::endl;
    for (auto& sensor : sensors) {
        sensor->calibrate();
    }
    
    // Print reports using polymorphism
    std::cout << "\nSensor Reports:" << std::endl;
    for (const auto& sensor : sensors) {
        sensor->printReport();
        std::cout << "---" << std::endl;
    }
    
    // Demonstrate downcasting
    std::cout << "\nDowncasting example:" << std::endl;
    if (auto tempSensor = dynamic_cast<TemperatureSensor*>(sensors[0].get())) {
        tempSensor->setTemperatureRange(-20.0, 50.0);
    }
}
```

### Multiple Inheritance

```cpp
#include <iostream>
#include <string>

// First base class
class Configurable {
protected:
    std::string configFile;
    
public:
    Configurable(const std::string& config = "default.conf") : configFile(config) {}
    
    virtual void loadConfiguration() {
        std::cout << "Loading configuration from " << configFile << std::endl;
    }
    
    virtual void saveConfiguration() {
        std::cout << "Saving configuration to " << configFile << std::endl;
    }
    
    std::string getConfigFile() const { return configFile; }
};

// Second base class
class Networkable {
protected:
    std::string ipAddress;
    int port;
    
public:
    Networkable(const std::string& ip = "127.0.0.1", int p = 8080) 
        : ipAddress(ip), port(p) {}
    
    virtual void connect() {
        std::cout << "Connecting to " << ipAddress << ":" << port << std::endl;
    }
    
    virtual void disconnect() {
        std::cout << "Disconnecting from " << ipAddress << ":" << port << std::endl;
    }
    
    virtual void sendData(const std::string& data) {
        std::cout << "Sending data: " << data << " to " << ipAddress << std::endl;
    }
    
    std::string getAddress() const { return ipAddress + ":" + std::to_string(port); }
};

// Multiple inheritance
class SmartSensor : public Sensor, public Configurable, public Networkable {
private:
    std::string firmwareVersion;
    
public:
    SmartSensor(const std::string& id, const std::string& ip, int port)
        : Sensor(id), 
          Configurable(id + ".conf"), 
          Networkable(ip, port),
          firmwareVersion("1.2.3") {
        std::cout << "SmartSensor constructor: " << sensorId << std::endl;
    }
    
    ~SmartSensor() override {
        std::cout << "SmartSensor destructor: " << sensorId << std::endl;
    }
    
    std::string getUnit() const override {
        return "units";
    }
    
    std::string getType() const override {
        return "Smart";
    }
    
    void calibrate() override {
        std::cout << "Remote calibrating smart sensor " << sensorId << std::endl;
        sendData("CALIBRATE_REQUEST");
        isCalibrated = true;
    }
    
    void initialize() {
        loadConfiguration();
        connect();
        calibrate();
    }
    
    void shutdown() {
        saveConfiguration();
        disconnect();
    }
    
    void uploadFirmware(const std::string& version) {
        std::cout << "Uploading firmware " << version << " to " << sensorId << std::endl;
        firmwareVersion = version;
        sendData("FIRMWARE_UPDATE:" + version);
    }
    
    void printReport() const override {
        Sensor::printReport();
        std::cout << "Network: " << getAddress() << std::endl;
        std::cout << "Config: " << getConfigFile() << std::endl;
        std::cout << "Firmware: " << firmwareVersion << std::endl;
    }
};

void demonstrateMultipleInheritance() {
    std::cout << "=== Multiple Inheritance Demo ===" << std::endl;
    
    SmartSensor sensor("SMART-01", "192.168.1.100", 8080);
    
    sensor.initialize();
    
    sensor.addReading(25.3);
    sensor.addReading(24.8);
    sensor.addReading(25.1);
    
    sensor.uploadFirmware("1.3.0");
    
    sensor.printReport();
    
    sensor.shutdown();
}
```

## Polymorphism

### Virtual Functions and Dynamic Binding

```cpp
#include <iostream>
#include <vector>
#include <memory>

class Shape {
protected:
    double x, y;  // Position
    
public:
    Shape(double posX, double posY) : x(posX), y(posY) {}
    virtual ~Shape() = default;
    
    // Pure virtual functions
    virtual double calculateArea() const = 0;
    virtual double calculatePerimeter() const = 0;
    virtual void draw() const = 0;
    
    // Virtual function with default implementation
    virtual void move(double deltaX, double deltaY) {
        x += deltaX;
        y += deltaY;
        std::cout << "Moving shape to (" << x << ", " << y << ")" << std::endl;
    }
    
    // Non-virtual function
    void getPosition(double& posX, double& posY) const {
        posX = x;
        posY = y;
    }
};

class Circle : public Shape {
private:
    double radius;
    
public:
    Circle(double x, double y, double r) : Shape(x, y), radius(r) {}
    
    double calculateArea() const override {
        return 3.14159 * radius * radius;
    }
    
    double calculatePerimeter() const override {
        return 2 * 3.14159 * radius;
    }
    
    void draw() const override {
        std::cout << "Drawing circle at (" << x << ", " << y 
                  << ") with radius " << radius << std::endl;
    }
    
    void move(double deltaX, double deltaY) override {
        Shape::move(deltaX, deltaY);  // Call base implementation
        std::cout << "Circle moved" << std::endl;
    }
};

class Rectangle : public Shape {
private:
    double width, height;
    
public:
    Rectangle(double x, double y, double w, double h) 
        : Shape(x, y), width(w), height(h) {}
    
    double calculateArea() const override {
        return width * height;
    }
    
    double calculatePerimeter() const override {
        return 2 * (width + height);
    }
    
    void draw() const override {
        std::cout << "Drawing rectangle at (" << x << ", " << y 
                  << ") with size " << width << "x" << height << std::endl;
    }
};

class Triangle : public Shape {
private:
    double base, height;
    
public:
    Triangle(double x, double y, double b, double h) 
        : Shape(x, y), base(b), height(h) {}
    
    double calculateArea() const override {
        return 0.5 * base * height;
    }
    
    double calculatePerimeter() const override {
        // Assuming equilateral triangle for simplicity
        return 3 * base;
    }
    
    void draw() const override {
        std::cout << "Drawing triangle at (" << x << ", " << y 
                  << ") with base " << base << " and height " << height << std::endl;
    }
};

void demonstratePolymorphism() {
    std::cout << "=== Polymorphism Demo ===" << std::endl;
    
    // Create shapes using polymorphism
    std::vector<std::unique_ptr<Shape>> shapes;
    
    shapes.push_back(std::make_unique<Circle>(10, 20, 5));
    shapes.push_back(std::make_unique<Rectangle>(0, 0, 10, 8));
    shapes.push_back(std::make_unique<Triangle>(15, 15, 6, 4));
    shapes.push_back(std::make_unique<Circle>(30, 30, 3));
    
    // Process all shapes polymorphically
    double totalArea = 0.0;
    double totalPerimeter = 0.0;
    
    std::cout << "Processing all shapes:" << std::endl;
    for (const auto& shape : shapes) {
        shape->draw();
        
        double area = shape->calculateArea();
        double perimeter = shape->calculatePerimeter();
        
        std::cout << "  Area: " << area << std::endl;
        std::cout << "  Perimeter: " << perimeter << std::endl;
        
        totalArea += area;
        totalPerimeter += perimeter;
        
        std::cout << "---" << std::endl;
    }
    
    std::cout << "Total area: " << totalArea << std::endl;
    std::cout << "Total perimeter: " << totalPerimeter << std::endl;
    
    // Demonstrate movement
    std::cout << "\nMoving all shapes by (5, -2):" << std::endl;
    for (auto& shape : shapes) {
        shape->move(5, -2);
    }
}
```

## Advanced OOP Concepts

### Operator Overloading

```cpp
#include <iostream>
#include <cmath>

class Vector3D {
private:
    double x, y, z;
    
public:
    // Constructors
    Vector3D() : x(0), y(0), z(0) {}
    Vector3D(double x, double y, double z) : x(x), y(y), z(z) {}
    
    // Accessor methods
    double getX() const { return x; }
    double getY() const { return y; }
    double getZ() const { return z; }
    
    // Arithmetic operators
    Vector3D operator+(const Vector3D& other) const {
        return Vector3D(x + other.x, y + other.y, z + other.z);
    }
    
    Vector3D operator-(const Vector3D& other) const {
        return Vector3D(x - other.x, y - other.y, z - other.z);
    }
    
    Vector3D operator*(double scalar) const {
        return Vector3D(x * scalar, y * scalar, z * scalar);
    }
    
    Vector3D operator/(double scalar) const {
        return Vector3D(x / scalar, y / scalar, z / scalar);
    }
    
    // Compound assignment operators
    Vector3D& operator+=(const Vector3D& other) {
        x += other.x;
        y += other.y;
        z += other.z;
        return *this;
    }
    
    Vector3D& operator-=(const Vector3D& other) {
        x -= other.x;
        y -= other.y;
        z -= other.z;
        return *this;
    }
    
    Vector3D& operator*=(double scalar) {
        x *= scalar;
        y *= scalar;
        z *= scalar;
        return *this;
    }
    
    // Comparison operators
    bool operator==(const Vector3D& other) const {
        const double epsilon = 1e-9;
        return std::abs(x - other.x) < epsilon && 
               std::abs(y - other.y) < epsilon && 
               std::abs(z - other.z) < epsilon;
    }
    
    bool operator!=(const Vector3D& other) const {
        return !(*this == other);
    }
    
    // Subscript operator
    double& operator[](int index) {
        switch (index) {
            case 0: return x;
            case 1: return y;
            case 2: return z;
            default: throw std::out_of_range("Vector3D index out of range");
        }
    }
    
    const double& operator[](int index) const {
        switch (index) {
            case 0: return x;
            case 1: return y;
            case 2: return z;
            default: throw std::out_of_range("Vector3D index out of range");
        }
    }
    
    // Stream operators (as friend functions)
    friend std::ostream& operator<<(std::ostream& os, const Vector3D& v) {
        os << "(" << v.x << ", " << v.y << ", " << v.z << ")";
        return os;
    }
    
    friend std::istream& operator>>(std::istream& is, Vector3D& v) {
        is >> v.x >> v.y >> v.z;
        return is;
    }
    
    // Utility methods
    double magnitude() const {
        return std::sqrt(x * x + y * y + z * z);
    }
    
    Vector3D normalize() const {
        double mag = magnitude();
        if (mag == 0) return Vector3D();
        return *this / mag;
    }
    
    double dot(const Vector3D& other) const {
        return x * other.x + y * other.y + z * other.z;
    }
    
    Vector3D cross(const Vector3D& other) const {
        return Vector3D(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }
};

// Non-member operator for scalar * vector
Vector3D operator*(double scalar, const Vector3D& vector) {
    return vector * scalar;
}

void demonstrateOperatorOverloading() {
    std::cout << "=== Operator Overloading Demo ===" << std::endl;
    
    Vector3D v1(1.0, 2.0, 3.0);
    Vector3D v2(4.0, 5.0, 6.0);
    
    std::cout << "v1 = " << v1 << std::endl;
    std::cout << "v2 = " << v2 << std::endl;
    
    // Arithmetic operations
    Vector3D v3 = v1 + v2;
    std::cout << "v1 + v2 = " << v3 << std::endl;
    
    Vector3D v4 = v2 - v1;
    std::cout << "v2 - v1 = " << v4 << std::endl;
    
    Vector3D v5 = v1 * 2.0;
    std::cout << "v1 * 2.0 = " << v5 << std::endl;
    
    Vector3D v6 = 3.0 * v1;
    std::cout << "3.0 * v1 = " << v6 << std::endl;
    
    // Compound assignment
    Vector3D v7 = v1;
    v7 += v2;
    std::cout << "v1 += v2 gives " << v7 << std::endl;
    
    // Subscript operator
    std::cout << "v1[0] = " << v1[0] << ", v1[1] = " << v1[1] << ", v1[2] = " << v1[2] << std::endl;
    
    // Comparison
    Vector3D v8(1.0, 2.0, 3.0);
    std::cout << "v1 == v8: " << (v1 == v8) << std::endl;
    std::cout << "v1 == v2: " << (v1 == v2) << std::endl;
    
    // Vector operations
    std::cout << "v1 magnitude: " << v1.magnitude() << std::endl;
    std::cout << "v1 normalized: " << v1.normalize() << std::endl;
    std::cout << "v1 dot v2: " << v1.dot(v2) << std::endl;
    std::cout << "v1 cross v2: " << v1.cross(v2) << std::endl;
}
```

## Next Steps

You now understand C++ object-oriented programming fundamentals. Continue with:

- **[C++ Memory Management](cpp-memory-management)** - Pointers, references, and smart pointers
- **[C++ Best Practices](cpp-best-practices)** - Modern C++ techniques and design patterns
- **[Python Overview](../python/python-overview)** - Compare with Python's OOP approach

Object-oriented programming in C++ provides powerful tools for modeling complex data processing systems with clean, maintainable code!