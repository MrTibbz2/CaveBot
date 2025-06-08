#include "serial_handler.h"
#include <cstring>
#include <stdio.h>
#include "pico/multicore.h"
#include <cctype>

#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h"
#define MAX_MESSAGE_LENGTH 16
status::SystemState status::currentState;
// Example function implementations
int executeGetState() {
    // Assuming currentState is a static member of status
    if (status::currentState.isConnected) { printf("USB_Serial: OK\n"); } else { return 1; }
    if (status::currentState.systemHealthy) { printf("System: Healthy\n"); } else { printf("System: Unhealthy"); }
    if (status::currentState.lastError == "none") { printf("lastError: none\n"); } else { printf("lastError: %s\n", status::currentState.lastError); }
    if (status::currentState.Core1Status[0] != '\0') { printf("Core1 Status: %s\n", status::currentState.Core1Status); } else { printf("Core1 Status: Not Running\n"); }

    if (status::currentState.readyForCommand) { printf("Commands: Ready\n"); } else { printf("Commands: Pending\n"); }
    
    if (status::currentState.lastCommand[0] != '\0') { printf("Last Command: %s\n", status::currentState.lastCommand); } else { printf("Last Command: None\n"); }
    return 0;
}

int executeInitAll() {

    return 0;
}

// Constructor or initialization function for commands
commands::commands() {
    // Set up getState command
    std::strcpy(getState.commandCall, "GET_STATE");
    std::strcpy(getState.name, "Get State");
    getState.execution = &executeGetState;

    // Set up InitAll command
    std::strcpy(InitAll.commandCall, "INIT_ALL");
    std::strcpy(InitAll.name, "Initialize All");
    InitAll.execution = &executeInitAll;

    // Update ExecutableCommands array if needed
    ExecutableCommands[0] = getState;
    ExecutableCommands[1] = InitAll;
}
commands::Command commands::checkCommands(char* command) {
    // Check if the command is valid and return it
    
    for (int i = 0; i < sizeof(ExecutableCommands) / sizeof(ExecutableCommands[0]); i++) {
        if (std::strcmp(command, ExecutableCommands[i].commandCall) == 0) {
            return ExecutableCommands[i]; // Return the matching command
        }
    }
    // Return an empty Command if no match found
    return Command();
}
int commands::ExecuteCommand(commands::Command command) {
    // Execute the command if it has an execution function
    if (command.execution != nullptr) {
        return command.execution();
    } else {
        std::strcpy(status::currentState.lastError, "err: no_exec");
        return 1; // Indicate error
    }
}

char* commands::ReadBufferuntilCommand(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()) {
    if (!status::currentState.initialised) {
        static char ret[18] = "err: un_init";
        strcpy(status::currentState.lastError, ret);
        static char error_ret[6] = "error"; // Use a static char buffer for error
        return error_ret; // Return the non-const buffer
    }
    char message[17] = "";
    static char input[MAX_MESSAGE_LENGTH + 1] = ""; // Buffer for incoming message
    unsigned int message_pos = 0;
    bool GotCommand = false;
    while (true) {
        if (!tud_cdc_connected()) {
            status::currentState.isConnected = false;
            sleep_ms(100);
            continue; // Wait until connected
            

        }
        if (status::currentState.isConnected == false) {
            printf("INFO: listening_for_commands\n");
            status::currentState.isConnected = true;
        }
        
        while (!GotCommand) {
            while (tud_cdc_available()) {
                char inByte = getchar();  // Read one character at a time

                // Add the character to the buffer unless it's a newline
                if (inByte != '\n' && message_pos < MAX_MESSAGE_LENGTH) {
                    input[message_pos++] = inByte;
                } else { 
                    // Null-terminate and print when a newline is received
                    input[message_pos] = '\0';
                    GotCommand = true;
                    
                    
                }
                
            }
        }
        for (int i = message_pos - 1; i >= 0; i--) {
            if (isspace(input[i]) || input[i] == '\r' || input[i] == '\n') {
                input[i] = '\0';
            } else {
                break;
            }
        }

        return input;

    }
}
