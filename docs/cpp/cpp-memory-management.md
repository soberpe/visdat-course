---
title: C++ Memory Management
---

# C++ Memory Management

## Understanding Memory in C++

Memory management is one of C++'s most powerful features, giving you direct control over how your program uses system resources.

### Stack vs Heap Memory

```cpp
#include <iostream>
#include <memory>

void demonstrateStackVsHeap() {
    std::cout << "=== Stack vs Heap Memory Demo ===" << std::endl;
    
    // Stack allocation - automatic cleanup
    {
        int stackVariable = 42;                    // On the stack
        double stackArray[100];                    // Fixed-size array on stack
        
        std::cout << "Stack variable address: " << &stackVariable << std::endl;
        std::cout << "Stack array address: " << stackArray << std::endl;
        
        // Variables automatically destroyed when leaving this scope
    }
    // stackVariable and stackArray are automatically cleaned up here
    
    // Heap allocation - manual management required (avoid raw pointers)
    int* heapVariable = new int(42);              // Dynamic allocation
    double* heapArray = new double[100];          // Dynamic array
    
    std::cout << "Heap variable address: " << heapVariable << std::endl;
    std::cout << "Heap variable value: " << *heapVariable << std::endl;
    std::cout << "Heap array address: " << heapArray << std::endl;
    
    // Manual cleanup required
    delete heapVariable;
    delete[] heapArray;  // Note: delete[] for arrays
    
    // Smart pointers - automatic cleanup (preferred approach)
    std::unique_ptr<int> smartPtr = std::make_unique<int>(42);
    std::unique_ptr<double[]> smartArray = std::make_unique<double[]>(100);
    
    std::cout << "Smart pointer value: " << *smartPtr << std::endl;
    std::cout << "Smart array address: " << smartArray.get() << std::endl;
    
    // Automatic cleanup when smartPtr and smartArray go out of scope
}
```

### Stack Memory Characteristics

```cpp
#include <iostream>
#include <chrono>

class StackExample {
private:
    double data[1000];  // 8KB on stack
    int size;
    
public:
    StackExample() : size(1000) {
        // Initialize with sample data
        for (int i = 0; i < size; ++i) {
            data[i] = i * 0.1;
        }
    }
    
    double calculateSum() const {
        double sum = 0.0;
        for (int i = 0; i < size; ++i) {
            sum += data[i];
        }
        return sum;
    }
    
    void printInfo() const {
        std::cout << "Stack object size: " << sizeof(*this) << " bytes" << std::endl;
        std::cout << "Array address: " << data << std::endl;
        std::cout << "Sum of elements: " << calculateSum() << std::endl;
    }
};

void demonstrateStackCharacteristics() {
    std::cout << "=== Stack Memory Characteristics ===" << std::endl;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    // Fast allocation/deallocation
    for (int i = 0; i < 10000; ++i) {
        StackExample obj;  // Very fast allocation
        double sum = obj.calculateSum();
        // Automatic deallocation when obj goes out of scope
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "10,000 stack allocations took: " << duration.count() << " microseconds" << std::endl;
    
    // Demonstrate automatic cleanup
    {
        StackExample localObj;
        localObj.printInfo();
        std::cout << "Object will be automatically destroyed at end of scope" << std::endl;
    }
    std::cout << "Object has been destroyed" << std::endl;
}
```

## Pointers and References

### Basic Pointer Operations

```cpp
#include <iostream>

void demonstrateBasicPointers() {
    std::cout << "=== Basic Pointer Operations ===" << std::endl;
    
    // Basic pointer usage
    int value = 42;
    int* ptr = &value;          // ptr points to value
    int** ptrToPtr = &ptr;      // Pointer to pointer
    
    std::cout << "Value: " << value << std::endl;
    std::cout << "Value address: " << &value << std::endl;
    std::cout << "Pointer value (address): " << ptr << std::endl;
    std::cout << "Dereferenced pointer: " << *ptr << std::endl;
    std::cout << "Pointer address: " << &ptr << std::endl;
    std::cout << "Pointer to pointer: " << ptrToPtr << std::endl;
    std::cout << "Double dereferenced: " << **ptrToPtr << std::endl;
    
    // Modifying through pointer
    *ptr = 100;
    std::cout << "After *ptr = 100, value = " << value << std::endl;
    
    // Null pointer
    int* nullPtr = nullptr;
    std::cout << "Null pointer: " << nullPtr << std::endl;
    
    // Pointer arithmetic
    int array[5] = {10, 20, 30, 40, 50};
    int* arrayPtr = array;
    
    std::cout << "\nPointer arithmetic:" << std::endl;
    for (int i = 0; i < 5; ++i) {
        std::cout << "array[" << i << "] = " << *(arrayPtr + i) 
                  << " at address " << (arrayPtr + i) << std::endl;
    }
    
    // Moving pointer
    std::cout << "\nMoving pointer through array:" << std::endl;
    arrayPtr = array;
    while (arrayPtr < array + 5) {
        std::cout << "Value: " << *arrayPtr << " at " << arrayPtr << std::endl;
        ++arrayPtr;
    }
}
```

### References

```cpp
#include <iostream>

void demonstrateReferences() {
    std::cout << "=== References Demo ===" << std::endl;
    
    int original = 42;
    int& reference = original;  // Reference must be initialized
    
    std::cout << "Original value: " << original << std::endl;
    std::cout << "Reference value: " << reference << std::endl;
    std::cout << "Original address: " << &original << std::endl;
    std::cout << "Reference address: " << &reference << std::endl;
    
    // Modifying through reference
    reference = 100;
    std::cout << "After reference = 100:" << std::endl;
    std::cout << "Original value: " << original << std::endl;
    std::cout << "Reference value: " << reference << std::endl;
    
    // References in function parameters
    auto swapByReference = [](int& a, int& b) {
        int temp = a;
        a = b;
        b = temp;
    };
    
    auto swapByPointer = [](int* a, int* b) {
        int temp = *a;
        *a = *b;
        *b = temp;
    };
    
    int x = 10, y = 20;
    std::cout << "\nBefore swap: x = " << x << ", y = " << y << std::endl;
    
    swapByReference(x, y);
    std::cout << "After reference swap: x = " << x << ", y = " << y << std::endl;
    
    swapByPointer(&x, &y);
    std::cout << "After pointer swap: x = " << x << ", y = " << y << std::endl;
}
```

### Pointer vs Reference Comparison

```cpp
#include <iostream>
#include <vector>

class DataProcessor {
private:
    std::vector<double> data;
    
public:
    // Using const reference (preferred for large objects)
    void processDataByConstRef(const std::vector<double>& inputData) {
        std::cout << "Processing " << inputData.size() << " elements by const reference" << std::endl;
        // Cannot modify inputData
        data = inputData;  // Copy to internal storage
    }
    
    // Using reference (for modification)
    void normalizeDataByRef(std::vector<double>& inputData) {
        std::cout << "Normalizing " << inputData.size() << " elements by reference" << std::endl;
        
        double sum = 0.0;
        for (const auto& value : inputData) {
            sum += value;
        }
        double mean = sum / inputData.size();
        
        for (auto& value : inputData) {
            value -= mean;  // Modifies original data
        }
    }
    
    // Using pointer (can be null, can be reassigned)
    void analyzeDataByPtr(const double* dataPtr, size_t size) {
        if (dataPtr == nullptr) {
            std::cout << "Null pointer provided, cannot analyze" << std::endl;
            return;
        }
        
        std::cout << "Analyzing " << size << " elements by pointer" << std::endl;
        
        double min = dataPtr[0];
        double max = dataPtr[0];
        
        for (size_t i = 1; i < size; ++i) {
            if (dataPtr[i] < min) min = dataPtr[i];
            if (dataPtr[i] > max) max = dataPtr[i];
        }
        
        std::cout << "Range: [" << min << ", " << max << "]" << std::endl;
    }
    
    void printData() const {
        std::cout << "Internal data: ";
        for (const auto& value : data) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }
};

void demonstratePointerVsReference() {
    std::cout << "=== Pointer vs Reference Comparison ===" << std::endl;
    
    DataProcessor processor;
    std::vector<double> testData = {1.5, 2.3, 4.1, 3.8, 2.9, 5.2, 1.7};
    
    std::cout << "Original data: ";
    for (const auto& value : testData) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
    
    // Const reference - safe, no copying, cannot modify
    processor.processDataByConstRef(testData);
    processor.printData();
    
    // Reference - can modify original
    std::vector<double> dataCopy = testData;
    processor.normalizeDataByRef(dataCopy);
    std::cout << "After normalization: ";
    for (const auto& value : dataCopy) {
        std::cout << value << " ";
    }
    std::cout << std::endl;
    
    // Pointer - flexible but requires null checking
    processor.analyzeDataByPtr(testData.data(), testData.size());
    processor.analyzeDataByPtr(nullptr, 0);  // Test null pointer
}
```

## Smart Pointers

### unique_ptr

```cpp
#include <iostream>
#include <memory>
#include <vector>

class SensorData {
private:
    std::string sensorId;
    std::vector<double> readings;
    
public:
    SensorData(const std::string& id) : sensorId(id) {
        std::cout << "SensorData created: " << sensorId << std::endl;
    }
    
    ~SensorData() {
        std::cout << "SensorData destroyed: " << sensorId << std::endl;
    }
    
    void addReading(double value) {
        readings.push_back(value);
    }
    
    size_t getCount() const {
        return readings.size();
    }
    
    std::string getId() const {
        return sensorId;
    }
    
    double getAverage() const {
        if (readings.empty()) return 0.0;
        
        double sum = 0.0;
        for (const auto& reading : readings) {
            sum += reading;
        }
        return sum / readings.size();
    }
};

void demonstrateUniquePtr() {
    std::cout << "=== unique_ptr Demo ===" << std::endl;
    
    // Create unique_ptr
    std::unique_ptr<SensorData> sensor1 = std::make_unique<SensorData>("TEMP-01");
    
    // Use like regular pointer
    sensor1->addReading(22.5);
    sensor1->addReading(23.1);
    sensor1->addReading(22.8);
    
    std::cout << "Sensor " << sensor1->getId() 
              << " has " << sensor1->getCount() << " readings" << std::endl;
    std::cout << "Average: " << sensor1->getAverage() << "°C" << std::endl;
    
    // Move ownership (unique_ptr cannot be copied)
    std::unique_ptr<SensorData> sensor2 = std::move(sensor1);
    
    std::cout << "After move:" << std::endl;
    std::cout << "sensor1 is " << (sensor1 ? "valid" : "null") << std::endl;
    std::cout << "sensor2 is " << (sensor2 ? "valid" : "null") << std::endl;
    
    if (sensor2) {
        std::cout << "sensor2 ID: " << sensor2->getId() << std::endl;
    }
    
    // Release ownership
    SensorData* rawPtr = sensor2.release();
    std::cout << "After release, sensor2 is " << (sensor2 ? "valid" : "null") << std::endl;
    std::cout << "Raw pointer ID: " << rawPtr->getId() << std::endl;
    
    // Must manually delete when using release()
    delete rawPtr;
    
    // Create array of unique_ptrs
    std::vector<std::unique_ptr<SensorData>> sensors;
    sensors.push_back(std::make_unique<SensorData>("TEMP-02"));
    sensors.push_back(std::make_unique<SensorData>("TEMP-03"));
    sensors.push_back(std::make_unique<SensorData>("TEMP-04"));
    
    for (auto& sensor : sensors) {
        sensor->addReading(20.0 + (rand() % 100) / 10.0);
        std::cout << "Sensor " << sensor->getId() 
                  << " reading: " << sensor->getAverage() << "°C" << std::endl;
    }
    
    // Automatic cleanup when vector goes out of scope
}
```

### shared_ptr

```cpp
#include <iostream>
#include <memory>
#include <vector>

class DataLogger {
private:
    std::string filename;
    
public:
    DataLogger(const std::string& file) : filename(file) {
        std::cout << "DataLogger created: " << filename << std::endl;
    }
    
    ~DataLogger() {
        std::cout << "DataLogger destroyed: " << filename << std::endl;
    }
    
    void log(const std::string& message) {
        std::cout << "[" << filename << "] " << message << std::endl;
    }
    
    std::string getFilename() const {
        return filename;
    }
};

class SensorWithLogger {
private:
    std::string sensorId;
    std::shared_ptr<DataLogger> logger;
    
public:
    SensorWithLogger(const std::string& id, std::shared_ptr<DataLogger> log) 
        : sensorId(id), logger(log) {
        logger->log("Sensor " + sensorId + " created");
    }
    
    ~SensorWithLogger() {
        if (logger) {
            logger->log("Sensor " + sensorId + " destroyed");
        }
    }
    
    void takeReading(double value) {
        logger->log("Sensor " + sensorId + " reading: " + std::to_string(value));
    }
    
    std::shared_ptr<DataLogger> getLogger() const {
        return logger;  // Safe to return shared_ptr
    }
};

void demonstrateSharedPtr() {
    std::cout << "=== shared_ptr Demo ===" << std::endl;
    
    // Create shared logger
    std::shared_ptr<DataLogger> logger = std::make_shared<DataLogger>("system.log");
    std::cout << "Logger reference count: " << logger.use_count() << std::endl;
    
    // Share logger among multiple sensors
    std::vector<std::unique_ptr<SensorWithLogger>> sensors;
    
    sensors.push_back(std::make_unique<SensorWithLogger>("TEMP-01", logger));
    std::cout << "After creating TEMP-01, reference count: " << logger.use_count() << std::endl;
    
    sensors.push_back(std::make_unique<SensorWithLogger>("TEMP-02", logger));
    std::cout << "After creating TEMP-02, reference count: " << logger.use_count() << std::endl;
    
    sensors.push_back(std::make_unique<SensorWithLogger>("TEMP-03", logger));
    std::cout << "After creating TEMP-03, reference count: " << logger.use_count() << std::endl;
    
    // Use sensors
    for (int i = 0; i < sensors.size(); ++i) {
        sensors[i]->takeReading(20.0 + i * 2.5);
    }
    
    // Create additional shared_ptr
    std::shared_ptr<DataLogger> anotherRef = sensors[0]->getLogger();
    std::cout << "After creating another reference, count: " << logger.use_count() << std::endl;
    
    // Remove one sensor
    sensors.erase(sensors.begin());
    std::cout << "After removing TEMP-01, reference count: " << logger.use_count() << std::endl;
    
    // Logger will be destroyed when last shared_ptr is destroyed
    anotherRef.reset();  // Explicitly release reference
    std::cout << "After resetting anotherRef, count: " << logger.use_count() << std::endl;
    
    // Clear all sensors
    sensors.clear();
    std::cout << "After clearing sensors, count: " << logger.use_count() << std::endl;
    
    // Reset original logger reference
    logger.reset();
    std::cout << "Logger should be destroyed now" << std::endl;
}
```

### weak_ptr

```cpp
#include <iostream>
#include <memory>

class Node {
private:
    int data;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> parent;  // Weak reference to avoid cycles
    
public:
    Node(int value) : data(value) {
        std::cout << "Node " << data << " created" << std::endl;
    }
    
    ~Node() {
        std::cout << "Node " << data << " destroyed" << std::endl;
    }
    
    void setNext(std::shared_ptr<Node> nextNode) {
        next = nextNode;
        if (next) {
            next->parent = shared_from_this();
        }
    }
    
    std::shared_ptr<Node> getNext() const {
        return next;
    }
    
    std::shared_ptr<Node> getParent() const {
        return parent.lock();  // Convert weak_ptr to shared_ptr safely
    }
    
    int getData() const {
        return data;
    }
    
    void printInfo() const {
        std::cout << "Node " << data;
        if (next) {
            std::cout << " -> " << next->getData();
        } else {
            std::cout << " -> null";
        }
        
        if (auto parentPtr = parent.lock()) {
            std::cout << " (parent: " << parentPtr->getData() << ")";
        } else {
            std::cout << " (no parent)";
        }
        std::cout << std::endl;
    }
};

// Need to inherit from enable_shared_from_this for shared_from_this() to work
class SafeNode : public std::enable_shared_from_this<SafeNode> {
private:
    int data;
    std::shared_ptr<SafeNode> next;
    std::weak_ptr<SafeNode> parent;
    
public:
    SafeNode(int value) : data(value) {
        std::cout << "SafeNode " << data << " created" << std::endl;
    }
    
    ~SafeNode() {
        std::cout << "SafeNode " << data << " destroyed" << std::endl;
    }
    
    void setNext(std::shared_ptr<SafeNode> nextNode) {
        next = nextNode;
        if (next) {
            next->parent = shared_from_this();
        }
    }
    
    std::shared_ptr<SafeNode> getNext() const {
        return next;
    }
    
    std::shared_ptr<SafeNode> getParent() const {
        return parent.lock();
    }
    
    int getData() const {
        return data;
    }
    
    void printChain() const {
        std::cout << "Chain from " << data << ": ";
        auto current = shared_from_this();
        while (current) {
            std::cout << current->getData() << " ";
            current = current->getNext();
        }
        std::cout << std::endl;
    }
};

void demonstrateWeakPtr() {
    std::cout << "=== weak_ptr Demo ===" << std::endl;
    
    // Create a chain of nodes
    auto node1 = std::make_shared<SafeNode>(1);
    auto node2 = std::make_shared<SafeNode>(2);
    auto node3 = std::make_shared<SafeNode>(3);
    
    std::cout << "Reference counts:" << std::endl;
    std::cout << "node1: " << node1.use_count() << std::endl;
    std::cout << "node2: " << node2.use_count() << std::endl;
    std::cout << "node3: " << node3.use_count() << std::endl;
    
    // Link nodes
    node1->setNext(node2);
    node2->setNext(node3);
    
    std::cout << "\nAfter linking:" << std::endl;
    std::cout << "node1: " << node1.use_count() << std::endl;
    std::cout << "node2: " << node2.use_count() << std::endl;
    std::cout << "node3: " << node3.use_count() << std::endl;
    
    // Print chain
    node1->printChain();
    
    // Test weak_ptr functionality
    std::weak_ptr<SafeNode> weakRef = node2;
    std::cout << "\nCreated weak reference to node2" << std::endl;
    std::cout << "node2 use_count: " << node2.use_count() << std::endl;
    std::cout << "weak_ptr expired: " << weakRef.expired() << std::endl;
    
    // Access through weak_ptr
    if (auto lockedPtr = weakRef.lock()) {
        std::cout << "Weak reference valid, data: " << lockedPtr->getData() << std::endl;
    }
    
    // Remove strong reference
    node2.reset();
    std::cout << "\nAfter resetting node2:" << std::endl;
    std::cout << "weak_ptr expired: " << weakRef.expired() << std::endl;
    
    if (auto lockedPtr = weakRef.lock()) {
        std::cout << "Weak reference still valid" << std::endl;
    } else {
        std::cout << "Weak reference is now invalid" << std::endl;
    }
    
    // Nodes will be properly destroyed when going out of scope
}
```

## RAII (Resource Acquisition Is Initialization)

```cpp
#include <iostream>
#include <fstream>
#include <vector>
#include <stdexcept>

class FileManager {
private:
    std::fstream file;
    std::string filename;
    
public:
    FileManager(const std::string& name, std::ios::openmode mode = std::ios::in | std::ios::out) 
        : filename(name) {
        file.open(filename, mode);
        if (!file.is_open()) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
        std::cout << "File opened: " << filename << std::endl;
    }
    
    ~FileManager() {
        if (file.is_open()) {
            file.close();
            std::cout << "File closed: " << filename << std::endl;
        }
    }
    
    // Delete copy operations to prevent multiple file handles
    FileManager(const FileManager&) = delete;
    FileManager& operator=(const FileManager&) = delete;
    
    // Move operations
    FileManager(FileManager&& other) noexcept 
        : file(std::move(other.file)), filename(std::move(other.filename)) {
        std::cout << "File moved: " << filename << std::endl;
    }
    
    FileManager& operator=(FileManager&& other) noexcept {
        if (this != &other) {
            if (file.is_open()) {
                file.close();
            }
            file = std::move(other.file);
            filename = std::move(other.filename);
            std::cout << "File move-assigned: " << filename << std::endl;
        }
        return *this;
    }
    
    void writeData(const std::vector<double>& data) {
        for (const auto& value : data) {
            file << value << " ";
        }
        file << std::endl;
        file.flush();
    }
    
    std::vector<double> readData() {
        std::vector<double> data;
        file.seekg(0, std::ios::beg);  // Go to beginning
        
        double value;
        while (file >> value) {
            data.push_back(value);
        }
        
        file.clear();  // Clear EOF flag
        return data;
    }
    
    bool isOpen() const {
        return file.is_open();
    }
};

class MemoryPool {
private:
    double* pool;
    size_t size;
    size_t used;
    
public:
    MemoryPool(size_t poolSize) : size(poolSize), used(0) {
        pool = new double[size];
        std::cout << "Memory pool allocated: " << size * sizeof(double) << " bytes" << std::endl;
    }
    
    ~MemoryPool() {
        delete[] pool;
        std::cout << "Memory pool deallocated" << std::endl;
    }
    
    // Delete copy operations
    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;
    
    double* allocate(size_t count) {
        if (used + count > size) {
            throw std::runtime_error("Memory pool exhausted");
        }
        
        double* ptr = pool + used;
        used += count;
        std::cout << "Allocated " << count << " doubles from pool" << std::endl;
        return ptr;
    }
    
    void reset() {
        used = 0;
        std::cout << "Memory pool reset" << std::endl;
    }
    
    size_t getUsed() const { return used; }
    size_t getSize() const { return size; }
};

void demonstrateRAII() {
    std::cout << "=== RAII Demo ===" << std::endl;
    
    try {
        // File resource management
        {
            FileManager fileManager("sensor_data.txt", std::ios::out | std::ios::trunc);
            
            std::vector<double> sensorData = {22.5, 23.1, 22.8, 23.4, 22.9};
            fileManager.writeData(sensorData);
            
            std::cout << "Data written to file" << std::endl;
            // File automatically closed when fileManager goes out of scope
        }
        
        // Memory resource management
        {
            MemoryPool pool(1000);
            
            double* array1 = pool.allocate(100);
            double* array2 = pool.allocate(200);
            
            // Initialize arrays
            for (int i = 0; i < 100; ++i) {
                array1[i] = i * 0.1;
            }
            for (int i = 0; i < 200; ++i) {
                array2[i] = i * 0.2;
            }
            
            std::cout << "Pool usage: " << pool.getUsed() << "/" << pool.getSize() << std::endl;
            
            // No need to manually free - pool handles it
            // Memory automatically freed when pool goes out of scope
        }
        
        // Reading data back
        {
            FileManager fileReader("sensor_data.txt", std::ios::in);
            auto readData = fileReader.readData();
            
            std::cout << "Read " << readData.size() << " values: ";
            for (const auto& value : readData) {
                std::cout << value << " ";
            }
            std::cout << std::endl;
        }
        
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
    
    std::cout << "All resources automatically cleaned up" << std::endl;
}
```

## Next Steps

You now understand C++ memory management fundamentals including stack vs heap, pointers, references, smart pointers, and RAII. Continue with:

- **[C++ Best Practices](cpp-best-practices)** - Modern C++ techniques and design patterns
- **[Python Overview](../python/python-overview)** - Compare memory management approaches
- **[Programming Fundamentals](../programming/paradigms)** - Understand broader programming concepts

Proper memory management is crucial for building efficient, reliable data processing applications in C++!