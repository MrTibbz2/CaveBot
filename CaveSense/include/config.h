#include <array>
#include <string>

struct SensorConfig {
    uint8_t triggerPin;
    uint8_t echoPin;
    std::string name;
};

const std::array<SensorConfig, 8> SENSOR_CONFIG = {{
    {1, 0, "frontleft"},
    {3, 2, "frontright"},
    {5, 4, "leftfront"},
    {7, 6, "leftback"},
    {17, 16, "rightfront"},
    {19, 18, "rightback"},
    {21, 20, "backleft"},
    {9, 8, "backright"},
}};