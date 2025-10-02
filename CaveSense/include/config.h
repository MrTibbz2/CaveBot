#include "distance_sensor.h"
#include <array>
#include "hardware/pio.h"
struct SensorConfig {
    uint8_t triggerPin;
    uint8_t echoPin;
    PIO pio;
    uint sm;
};

const std::array<SensorConfig, 1> SENSOR_CONFIG = {{ // echo must me trigger + 1
    {0, 1, pio0, 0},   // Sensor 0
}};