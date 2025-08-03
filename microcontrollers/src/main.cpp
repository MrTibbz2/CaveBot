// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

#include <stdio.h>
#include "pico/multicore.h"
#include "serial_handler.h"
#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h" // YES!!!
#include <cstdlib>



#define PICO_LED_PIN 25

// Function to turn the onboard LED ON
void led_on() {
    gpio_put(PICO_LED_PIN, 1); // Set GPIO high to turn LED on
}

// Function to turn the onboard LED OFF
void led_off() {
    gpio_put(PICO_LED_PIN, 0); // Set GPIO low to turn LED off
}

// Static variable to hold the function pointer for core1
static int (*core1_func)() = nullptr;
char Core1CommandName[17];
// Function to be launched on core1
void core1_entry() {
    if (core1_func) {
        int result = core1_func();
        if (result != 0) {
            char buff[32];
            snprintf(buff,sizeof(buff), "{\"command\": \"%s\"}", Core1CommandName);
            output::logData({
                LogIdentifier::CORE1,
                "exec_result",
                LogStatus::FAILURE,
                buff
            });

        } else {
            char buff[32];
            snprintf(buff,sizeof(buff), "{\"command\": \"%s\"}", Core1CommandName);
            output::logData({
                LogIdentifier::CORE1,
                "exec_result",
                LogStatus::SUCCESS,
                buff
            });

        }

        
        strcpy(Core1CommandName, "");
        status::setCore1Running(false);
    }
    else {
        char buff[32];
        snprintf(buff, sizeof(buff), "{\"command\": \"%s\", \"error\": \"unknown_command\"}", Core1CommandName);
        output::logData({
            LogIdentifier::CORE1,
            "exec_result",
            LogStatus::FAILURE,
            buff

        });
        strcpy(Core1CommandName, "");
        status::setCore1Running(false);
    }
}

// Define buffer sizes as constexpr for safety and clarity
constexpr size_t MAIN_INPUT_BUFFER_SIZE = 32; // Example size, adjust as needed

int main() {
    status::setInitialised(stdio_init_all());  // Use setter for initialised
    gpio_init(PICO_LED_PIN);
    gpio_set_dir(PICO_LED_PIN, GPIO_OUT);
    commands cmdHandler;
    // Wait for USB CDC connection
    while (!tud_cdc_connected()) {
        sleep_ms(100);
    }
    // Send ready message on connection
    if (!status::getCurrentState().isConnected && tud_cdc_available) {
        output::logData({
            LogIdentifier::INFO,
            "system_status",
            LogStatus::READY,
            "{\"is_connected\": true}"
        });
        status::setConnected(true);
        status::setInitialised(true);
        status::setReadyForCommand(true);
        bool led = true;
        led_on();
    }
    bool led = false;
    static char inputBuffer[MAIN_INPUT_BUFFER_SIZE] = {0};
    while (true) {
        char* stringcommand = cmdHandler.ReadBuffer(tud_cdc_connected, tud_cdc_available);
        if (stringcommand == "error") { led = !led; if (led) {led_off();} else {led_on();} sleep_ms(500); continue; }
        else {
            if (strcmp(stringcommand, "CMD_STATUS") == 0) {
                const char* inp = "GETSTATE";
                commands::Command statusCommand = cmdHandler.checkCommand((char*)inp);
                int result = cmdHandler.ExecuteCommand(statusCommand);
                if (result == 0) {
                    char payload[128];
                    snprintf(payload, sizeof(payload), "{ \"command_name\": \"%s\", \"message\": \"Command executed successfully.\" }", inp);
                    output::logData({LogIdentifier::COMMAND, "execution_result", LogStatus::SUCCESS, payload});
                }
            }
            if (strncmp(stringcommand, "CMD_START_", 10) == 0) {
                const char* search_pattern = "CMD_START_";
                char result_buffer[17];
                const char* start_of_chars = strstr(stringcommand, search_pattern);
                start_of_chars += strlen(search_pattern);
                strncpy(result_buffer, start_of_chars, sizeof(result_buffer) - 1);
                result_buffer[sizeof(result_buffer) - 1] = '\0';
                commands::Command executable = cmdHandler.checkCommand(result_buffer);
                if (std::strcmp(executable.name, "NULL") == 0) {
                    char payload[12];
                    char buff[64];
                    snprintf(payload, sizeof(payload), result_buffer);
                    snprintf(buff, sizeof(buff), "{ \"error\": \"unknown_command\", \"command\": \"%s\" }", payload);
                    output::logData({
                        LogIdentifier::COMMAND,
                        "exec_result",
                        LogStatus::FAILURE,
                        buff
                    });
                } else {
                    if (!status::getCurrentCore1State().isRunning) {
                        core1_func = executable.execution;
                        strncpy(executable.name, Core1CommandName, sizeof(Core1CommandName));
                        status::setCore1Running(true);
                        
                        multicore_launch_core1(core1_entry);
                    } else {

                        
                        
                        output::logData({
                            LogIdentifier::CORE1,
                            "exec_result",
                            LogStatus::THREAD_LOCKED
                            
                    

                        });
                    }
                }
            }
        }
    }
    return 0;
}
