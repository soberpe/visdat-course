---
title: CMake & Build Systems
sidebar_position: 1
---

# CMake & Build Systems

## Why Build Systems Matter

When working with scientific computing and data visualization, you will eventually encounter compiled languages like C++ or need to use Python libraries that wrap C/C++ code for performance. Understanding build systems helps you work effectively in these environments.

## What is a Build System?

A build system automates the process of transforming source code into executable programs. For compiled languages like C++, this involves:

1. **Compiling** source files (.cpp) into object files (.o)
2. **Linking** object files together with libraries
3. **Managing dependencies** between files
4. **Configuring** platform-specific settings

### The Problem Without Build Systems

Imagine compiling a C++ project manually:

```bash
g++ -c src/main.cpp -o build/main.o -I include
g++ -c src/data_processor.cpp -o build/data_processor.o -I include  
g++ -c src/image_utils.cpp -o build/image_utils.o -I include
g++ build/main.o build/data_processor.o build/image_utils.o -o app -lopencv
```

This becomes unmaintainable for larger projects. What if you have 50 files? Different platforms? Optional features?

## What is CMake?

CMake is a **cross-platform build system generator**. It does not build your code directly. Instead, it generates build files for other tools (like Make on Linux, MSBuild on Windows, or Ninja on any platform).

### Key Concept

```
CMakeLists.txt → CMake → Makefile/VS Project → Build Tool → Executable
```

CMake acts as a meta-build system that abstracts platform differences.

## Basic CMake Example

### Simple Project Structure

```
my_project/
├── CMakeLists.txt
├── include/
│   └── calculator.h
└── src/
    ├── main.cpp
    └── calculator.cpp
```

### CMakeLists.txt

```cmake
# Minimum CMake version required
cmake_minimum_required(VERSION 3.10)

# Project name and version
project(Calculator VERSION 1.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add executable
add_executable(calculator 
    src/main.cpp
    src/calculator.cpp
)

# Include directories
target_include_directories(calculator PRIVATE include)
```

### Building the Project

```bash
# Create build directory
mkdir build
cd build

# Configure + Generate build files (no compilation yet)
cmake ..

# Build the project (actual compilation with g++/clang++/MSVC)
cmake --build .

# Run the executable
./calculator
```

**What happens:**
1. `cmake ..` - Configure project and generate build files (Makefile/VS solution)
2. `cmake --build .` - Run the build tool which compiles your code

:::tip Out-of-Source Builds
Always build in a separate `build/` directory. This keeps your source tree clean and allows multiple build configurations (Debug, Release, etc.).
:::

## CMake with External Libraries

Scientific computing often requires external libraries like OpenCV, Eigen, or VTK:

```cmake
cmake_minimum_required(VERSION 3.10)
project(ImageProcessor)

set(CMAKE_CXX_STANDARD 17)

# Find required packages
find_package(OpenCV REQUIRED)
find_package(Eigen3 REQUIRED)

# Add executable
add_executable(image_processor 
    src/main.cpp
    src/image_processor.cpp
)

# Link libraries
target_link_libraries(image_processor 
    ${OpenCV_LIBS}
    Eigen3::Eigen
)

# Include directories
target_include_directories(image_processor PRIVATE 
    include
    ${OpenCV_INCLUDE_DIRS}
)
```

## When You Encounter CMake as a Python User

### Installing Python Packages with C Extensions

Many Python libraries use C/C++ for performance-critical code. When you install these packages, they often need to be compiled:

```bash
pip install opencv-python  # May use CMake internally
pip install scipy          # Uses Fortran/C compilation
pip install numpy          # Compiled C extensions
```

:::note Pre-compiled Wheels
Most Python packages provide pre-compiled binaries (wheels) for common platforms, so you often don't need to build from source. But understanding the build process helps when things go wrong or you need custom builds.
:::

### Building Python Extensions

If you write performance-critical code in C++ and want to call it from Python, tools like **pybind11** or **Cython** often use CMake:

```cmake
# pybind11 example
find_package(pybind11 REQUIRED)

pybind11_add_module(my_module src/bindings.cpp src/fast_algorithm.cpp)
```

This creates a Python module that you can import:

```python
import my_module
result = my_module.fast_algorithm(data)
```

## CMake Project Structure Example

A well-organized C++ project using CMake:

```
fem_solver/
├── CMakeLists.txt              # Main build configuration
├── include/
│   └── fem_solver/
│       ├── mesh.h
│       ├── solver.h
│       └── element.h
├── src/
│   ├── main.cpp
│   ├── mesh.cpp
│   ├── solver.cpp
│   └── element.cpp
├── tests/
│   ├── CMakeLists.txt          # Test build configuration
│   ├── test_mesh.cpp
│   └── test_solver.cpp
├── external/                    # Third-party libraries
│   └── eigen/
└── build/                       # Build directory (git-ignored)
```

## Common CMake Commands

### Configuration & Generation
```bash
cmake -S . -B build              # Configure + generate (no compilation)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release  # Release mode
```

### Building (Compilation)
```bash
cmake --build build              # Compile with g++/clang++/MSVC
cmake --build build --target clean  # Clean build files
cmake --build build --parallel 8    # Parallel build (8 cores)
```

### Installation
```bash
cmake --install build --prefix /usr/local
```

## Why CMake Matters in Engineering

1. **Reproducible Builds**: Same source code builds consistently across platforms
2. **Dependency Management**: Automatically finds and links required libraries
3. **IDE Integration**: Most IDEs (Visual Studio, CLion, VS Code) understand CMake
4. **Industry Standard**: Used by major projects (OpenCV, VTK, KDE, Blender, etc.)

## Alternatives to CMake

- **Make**: Traditional Unix build tool (lower level, less portable)
- **Meson**: Modern, faster alternative (used by Python itself)
- **Bazel**: Google's build system (for very large projects)
- **xmake**: Lua-based build system (simpler syntax)

For most scientific computing projects, CMake remains the standard choice due to its maturity and ecosystem support.

## Key Takeaways

1. **Build systems automate compilation** for compiled languages
2. **CMake is a build system generator**, not a build system itself
3. **You'll encounter CMake** when:
   - Building C/C++ projects
   - Installing Python packages from source
   - Creating Python extensions for performance
4. **Basic workflow**: Write CMakeLists.txt → Run cmake → Build
5. **Out-of-source builds** keep your project clean

:::tip When to Learn More
You don't need to master CMake for Python-focused work. But understanding the basics helps when you need to:
- Build custom versions of libraries
- Debug installation issues
- Integrate C++ performance code with Python
- Collaborate on mixed-language projects
:::

## Further Reading

- [CMake Tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) - Official CMake tutorial
- [Modern CMake Guide](https://cliutils.gitlab.io/modern-cmake/) - Best practices
- [pybind11 Documentation](https://pybind11.readthedocs.io/) - Python/C++ bindings with CMake

