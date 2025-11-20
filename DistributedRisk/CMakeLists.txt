cmake_minimum_required(VERSION 3.10)

# Project Name
project(RiskEngine)

# Use C++17 (Modern Standard)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Tell CMake to take main.cpp and turn it into an executable named "RiskEngineExec"
add_executable(RiskEngineExec src/main.cpp)