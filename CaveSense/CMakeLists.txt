cmake_minimum_required(VERSION 3.13)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(PICO_SDK_PATH "${CMAKE_CURRENT_LIST_DIR}/pico-sdk")
include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(sensor_controller C CXX ASM)

pico_sdk_init()

add_executable(sensor_controller src/main.cpp src/serial_handler.cpp src/outdata.cpp src/distanceScan.cpp)

# Add your include directories
target_include_directories(sensor_controller
    PRIVATE
        "${CMAKE_CURRENT_LIST_DIR}/include"
        "${CMAKE_CURRENT_LIST_DIR}/hc-sr04-lib/include" # <-- Add this line
)

# Add the subdirectory so the library gets compiled
add_subdirectory(hc-sr04-lib)

# Link libraries
target_link_libraries(sensor_controller
    pico_stdlib
    distance-sensor
    pico_multicore # <-- Link the distance-sensor library
)

pico_add_extra_outputs(sensor_controller)
pico_enable_stdio_usb(sensor_controller 1)
pico_enable_stdio_uart(sensor_controller 0)
