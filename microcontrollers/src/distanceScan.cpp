#include "serial_handler.h"
#include <cstring>
#include <stdio.h>
#include "pico/multicore.h"
#include <cctype>
#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h"
const uint32_t interval_ms = 50;
void sensor::BeginSensorRead(int sensorcount, int* sensorpins) {
    DistanceSensor** sensors = new DistanceSensor*[sensorcount];
    for (int i = 0; i < sensorcount; ++i) {
        PIO pio = (i < 4) ? pio0 : pio1;
        int sm = i % 4; // 0-3 for each PIO
        sensors[i] = new DistanceSensor{pio, (uint)sm, (uint)sensorpins[i]}; // Cast to uint to avoid narrowing warning
    }

    for (int i = 0; i < sensorcount; ++i) {
        if (sensors[i] == nullptr) {
            char buff[32];

            snprintf(buff, sizeof(buff), "{\"error\": \"sensor_initialization_failed\", \"sensor_index\": %d}", i);
            output::logData({
                LogIdentifier::CORE1,
                "core1_status",
                LogStatus::SENSOR_FAULT,
                buff
            });
            for (int j = 0; j < i; ++j) {
                delete sensors[j];
            }
            delete[] sensors;
            return; // Early exit, no value
        }
        sensors[i]->TriggerRead(); // Start sensing

    }
    int* sensorreads = new int[sensorcount];
    while (!status::isCore1StopRequested) {
        uint32_t start = to_ms_since_boot(get_absolute_time());
        for (int i = 0; i < sensorcount; ++i) {
            if (!sensors[i]->is_sensing) {
                char buff[32];
                snprintf(buff, sizeof(buff), "{\"error\": \"sensor_failing\", \"sensor_index\": %d}", i);
                output::logData({
                    LogIdentifier::CORE1,
                    "core1_status",
                    LogStatus::SENSOR_FAULT,
                    buff
                });
            }
            if (sensors[i]->distance > 0) {
                sensorreads[i] = sensors[i]->distance;
            }
        }
        // Build JSON array of all sensor readings
        char* buff = new char[128 * sensorcount];
        memset(buff, 0, 128 * sensorcount); // Clear the buffer
        int pos = 0;
        pos += snprintf(buff + pos, 128 * sensorcount - pos, "[");
        for (int i = 0; i < sensorcount; ++i) {
            if (i > 0) pos += snprintf(buff + pos, 128 * sensorcount - pos, ", ");
            pos += snprintf(buff + pos, 128 * sensorcount - pos, "{\"sensor_id\": %d, \"distance_read\": %d}", i, sensorreads[i]);
        }
        pos += snprintf(buff + pos, 128 * sensorcount - pos, "]");
        output::logData({
            LogIdentifier::CORE1,
            "data_stream",
            LogStatus::ACTIVE,
            buff
        });
        delete[] buff;
        
        uint32_t elapsed = to_ms_since_boot(get_absolute_time()) - start;
        if (elapsed < interval_ms) {
        sleep_ms(interval_ms - elapsed); // Wait the remaining time
    }
    }
    
    
    //Remember to delete sensors when done to avoid memory leaks.
    for (int i = 0; i < sensorcount; ++i) {
        delete sensors[i];
    }
    delete[] sensors;
    delete[] sensorreads;
    
    
}
