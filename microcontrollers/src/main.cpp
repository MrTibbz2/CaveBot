#include <stdio.h>
#include "pico/multicore.h"
#include "serial_handler.h"
#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h" // YES!!!



#define PICO_LED_PIN 25

// Function to turn the onboard LED ON
void led_on() {
    gpio_put(PICO_LED_PIN, 1); // Set GPIO high to turn LED on
}

// Function to turn the onboard LED OFF
void led_off() {
    gpio_put(PICO_LED_PIN, 0); // Set GPIO low to turn LED off
}


int main() {
    status::currentState.initialised = stdio_init_all();  // Initialize USB serial I/O
    gpio_init(PICO_LED_PIN);
    gpio_set_dir(PICO_LED_PIN, GPIO_OUT);
    
    commands cmdHandler;  // Create an instance of the commands handler

    // Wait for USB CDC connection
    while (!tud_cdc_connected()) {
        sleep_ms(100);
    }

    // Send ready message on connection
    if (status::currentState.isConnected == false && tud_cdc_available) {
        output::logData(
            {
                LogIdentifier::INFO,
                "system_status",
                LogStatus::READY,
                "{\"is_connected\": true}"
            }
        );
        status::currentState.isConnected = true;
        status::currentState.initialised = true;
        status::currentState.readyForCommand = true;
    }

    bool led = false;
    while (true) {
        char* stringcommand = cmdHandler.ReadBuffer(tud_cdc_connected, tud_cdc_available);
        if (stringcommand == "error") { led = !led; if (led) {led_off;} else {led_on;} sleep_ms(500); continue;}
        else {
            if (strcmp(stringcommand, "CMD_STATUS") == 0) {
                // Assuming you want to execute the "status" command
                const char* inp = "GETSTATE";
                commands::Command statusCommand = cmdHandler.checkCommand((char*)inp);
                int result = cmdHandler.ExecuteCommand(statusCommand);
                if (result == 0) {
                    char payload[128];
                    snprintf(payload, sizeof(payload), "{ \"command_name\": \"%s\", \"message\": \"Command executed successfully.\" }", inp);
                    output::logData({LogIdentifier::COMMAND, "execution_result", LogStatus::SUCCESS, payload});
                }
            }
            if (strncmp(stringcommand, "CMD_START_", 10) == 0) {// checks if the received stringcommand is a CMD_START
                const char* search_pattern = "CMD_START_";
                char result_buffer[17]; // Ensure this is large enough

                const char* start_of_chars = strstr(stringcommand, search_pattern);
                start_of_chars += strlen(search_pattern);

                // Copy the actual command part into result_buffer
                // Use strncpy for safety: copies at most (sizeof(result_buffer) - 1) characters
                strncpy(result_buffer, start_of_chars, sizeof(result_buffer) - 1);
                
                // Ensure the string is null-terminated
                result_buffer[sizeof(result_buffer) - 1] = '\0';


                commands::Command executable = cmdHandler.checkCommand(result_buffer);
                if (std::strcmp(executable.name, "NULL") == 0) {
                    char payload[12];
                    char buff[64];
                    snprintf(payload, sizeof(payload), result_buffer);
                    snprintf(buff, sizeof(buff), "{ \"error\": \"unknown_command\", \"command\": \"%s\" }", payload);
                    output::logData(
                        {
                            LogIdentifier::COMMAND,
                            "exec_result",
                            LogStatus::FAILURE,
                            buff

                        }
                    );

                }
                else {
                    printf("stuff not ready to work yet but yeah will do!");
                    

                }
            }



        }



    }
    return 0;
}
