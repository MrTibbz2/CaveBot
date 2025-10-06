#include "distance_sensor.h"
#include <array>
#include "hardware/pio.h"
struct SensorConfig {
    uint8_t triggerPin;
    uint8_t echoPin;
    PIO pio;
    uint sm;
    std::string name;
};

const std::array<SensorConfig, 1> SENSOR_CONFIG = {{ // echo must be trigger - 1
    {1, 0, pio0, 0, "Front"},   // Sensor 0: trigger=1, echo=0
}};