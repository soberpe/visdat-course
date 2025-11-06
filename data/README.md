# Nova Paka Racing Dataset

## 🏎️ **Welcome to the Course Dataset!**

This dataset contains realistic racing telemetry data that you'll use throughout the **Visualization & Data Processing** course. All exercises will work with this consistent dataset, so you'll become familiar with the data structure while learning pandas operations.

## 📊 **Available Data Files**

You'll work with these files during the course:

### **racing_sessions.csv**
Session overview data with drivers, cars, and track conditions.

### **lap_times.csv** 
Individual lap performance data with sector times.

### **telemetry_detailed.csv**
High-resolution telemetry data from one complete lap.

### **nova_paka_racing_data.xlsx**
Excel format with multiple sheets for Excel I/O exercises.

### **racing_data.h5**
HDF5 format for advanced storage exercises.

## 🏁 **The Racing Context**

The dataset features:
- **Legendary rally drivers** like Walter Röhrl, Sébastien Loeb, and Tommi Mäkinen
- **Iconic rally cars** including Audi Quattro S1, Lancia Delta S4, and Ford RS200
- **Nova Paka track** (930m length, clay-sandy surface, 37m elevation change)
- **Authentic telemetry** with speed, RPM, steering, and G-force data

## 🎓 **How You'll Use This Data**

Throughout the course, you'll learn to:
- Load and explore the data using pandas
- Filter and analyze driver performance
- Compare different cars and weather conditions
- Visualize telemetry patterns
- Work with multiple file formats
- Optimize data storage and access

## 💡 **Getting Started**

Start with loading the session data:
```python
import pandas as pd
sessions = pd.read_csv('data/racing_sessions.csv')
print(sessions.head())
```

Happy data processing! �
