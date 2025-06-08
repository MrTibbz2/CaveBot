#include <stdio.h>
#include "pico/multicore.h"
#include "serial_handler.h"
#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h" // YES!!!

#define MAX_MESSAGE_LENGTH 16

int main() {
    status::currentState.initialised = stdio_init_all();  // Initialize USB serial I/O
    tud_cdc_available();
    tud_cdc_connected();
    commands cmdHandler;  // Create an instance of the commands handler
    while (true) {
        char* stringcommand = cmdHandler.ReadBufferuntilCommand(tud_cdc_connected, tud_cdc_available);
        if (strcmp(stringcommand, "error") == 0) {
            printf("Error reading input, lasterror: %s\n", status::currentState.lastError);
            continue;  // Skip to the next iteration if there was an error
        }
        strncpy(status::currentState.lastCommand, stringcommand, sizeof(status::currentState.lastCommand) - 1);
        status::currentState.lastCommand[sizeof(status::currentState.lastCommand) - 1] = '\0';  // Ensure null-termination
        commands::Command command = cmdHandler.checkCommands(stringcommand);  // Check if the command is valid
        
        if (command.commandCall[0] != '\0') {  // If a valid command was found
            int result = cmdHandler.ExecuteCommand(command);  // Execute the command
            if (result != 0) {
                printf("Command execution failed with error: %d\n", status::currentState.lastError);
            }
           else {
                printf("command %s exited succesfully.", status::currentState.lastCommand);  
            }
        } else {
            printf("Invalid command: %s\n", stringcommand);  // Handle invalid command
            strncpy(status::currentState.lastError, "err: no_cmd", sizeof(status::currentState.lastError) - 1);
            status::currentState.lastError[sizeof(status::currentState.lastError) - 1] = '\0';  // Ensure null-termination
        }

    }
    return 0;
}