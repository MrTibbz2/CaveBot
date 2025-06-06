cmake_minimum_required(VERSION 3.13)

set(PICO_SDK_PATH "${CMAKE_CURRENT_LIST_DIR}/pico-sdk")

include(${PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(sensor_controller C CXX ASM)

pico_sdk_init()

add_executable(sensor_controller src/main.cpp)

target_include_directories(sensor_controller PRIVATE "${CMAKE_CURRENT_LIST_DIR}/include")

target_link_libraries(sensor_controller pico_stdlib)

pico_add_extra_outputs(sensor_controller)

pico_enable_stdio_usb(sensor_controller 1)
pico_enable_stdio_uart(sensor_controller 0)