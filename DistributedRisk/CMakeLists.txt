cmake_minimum_required(VERSION 3.10)
project(RiskEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 1. Find where 'pybind11' is installed on your computer
execute_process(
    COMMAND python -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")

# 2. Load pybind11
find_package(pybind11 REQUIRED)

# 3. Create the module
# "risk_engine" will be the name you use in Python (import risk_engine)
pybind11_add_module(risk_engine src/main.cpp)