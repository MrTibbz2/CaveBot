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
status::Core1Status status::currentCore1State;
// Example function implementations

void output::get_string_until_delimiter(char* dest, const char* source, char delimiter, size_t dest_size) {
    if (dest == nullptr || source == nullptr || dest_size == 0) {
        if (dest != nullptr && dest_size > 0) dest[0] = '\0'; // Ensure it's null-terminated
        return;
    }

    const char* delimiter_pos = strchr(source, delimiter); // Find first occurrence of delimiter

    size_t length_to_copy;
    if (delimiter_pos != nullptr) {
        // Delimiter found: copy characters up to the delimiter
        length_to_copy = delimiter_pos - source;
    } else {
        // Delimiter not found: copy the entire string
        length_to_copy = strlen(source);
    }

    // Ensure we don't write past dest_size-1
    if (length_to_copy >= dest_size) {
        length_to_copy = dest_size - 1;
    }

    strncpy(dest, source, length_to_copy); // Copy the characters
    dest[length_to_copy] = '\0';            // Null-terminate the destination string
}

int executeGetState() {
    // OLD VERSION
    // if (status::currentState.isConnected) { printf("USB_Serial: OK\n"); } else { return 1; }
    // if (status::currentState.systemHealthy) { printf("System: Healthy\n"); } else { printf("System: Unhealthy"); }
    // if (status::currentState.Core1Status[0] != '\0') { printf("Core1 Status: %s\n", status::currentState.Core1Status); } else { printf("Core1 Status: Not Running\n"); }
    // if (status::currentState.readyForCommand) { printf("Commands: Ready\n"); } else { printf("Commands: Pending\n"); }
    // if (status::currentState.lastCommand[0] != '\0') { printf("Last Command: %s\n", status::currentState.lastCommand); } else { printf("Last Command: None\n"); }
    // OLD VERSION
    char status_payload_buffer[128];
    int payload_len = snprintf(status_payload_buffer, sizeof(status_payload_buffer),
                               "{ "
                                   "\"is_connected\": %s, "
                                   "\"initialised\": %s, "
                                   "\"ready_for_command\": %s, "
                                   "\"system_healthy\": \"%s\""
                               " }",
                               status::currentState.isConnected ? "true" : "false",
                               status::currentState.initialised ? "true" : "false",
                               status::currentState.readyForCommand ? "true" : "false",
                               status::currentState.systemHealthy ? "true" : "false"
                              );
    output::outdata status_log_data;
    if (status::currentState.initialised && status::currentState.readyForCommand && status::currentState.systemHealthy) {
        status_log_data.status_code = LogStatus::READY;
    } else if (!status::currentState.systemHealthy) {
        status_log_data.status_code = LogStatus::UNHEALTHY; // Or a more specific fault code
    } else if (status::currentState.systemHealthy) { status_log_data.status_code = LogStatus::INITIALISING; }
    status_log_data.identifier = LogIdentifier::INFO;          // This is an INFOrmational message
    status_log_data.message_type = "system_status";          // The type of info is about the system's general status
            
    status_log_data.payload_json = status_payload_buffer; // Additional details as JSON

    // Call logData to send this status message
    output::logData(status_log_data);
    return 0;
}

int executeInitAll() {

    return 0;
}

// Constructor or initialization function for commands
commands::commands() {
    // Set up getState command
    std::strcpy(getState.commandCall, "GETSTATE");
    std::strcpy(getState.name, "Get State");
    getState.execution = &executeGetState;

    // Set up InitAll command
    std::strcpy(InitAll.commandCall, "INITALL");
    std::strcpy(InitAll.name, "Initialize All");
    InitAll.execution = &executeInitAll;

    // Update ExecutableCommands array if needed
    ExecutableCommands[0] = getState;
    ExecutableCommands[1] = InitAll;
}
commands::Command commands::checkCommand(char* command) {
    // Check if the command is valid and return it
    
    for (int i = 0; i < sizeof(ExecutableCommands) / sizeof(ExecutableCommands[0]); i++) {
        if (std::strcmp(command, ExecutableCommands[i].commandCall) == 0) {
            return ExecutableCommands[i]; // Return the matching command
        }
    }
    commands::Command nullcmd;
    strcpy(nullcmd.name, "NULL");
    // Return an empty Command if no match found
    return nullcmd;
}
int commands::ExecuteCommand(commands::Command command) {
    // Execute the command if it has an execution function
    if (command.execution != nullptr) {
        return command.execution();
    } else {
        if (std::strcmp(command.name, "NULL") == 0) {
            printf("unknown command\n");
        }
        return 1; // Indicate error
    }
}

char* commands::ReadBuffer(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()) {
    if (!status::currentState.initialised) {
        
        static char error_ret[6] = "error"; // Use a static char buffer for error
        return error_ret; // Return the non-const buffer
    }
    char message[17] = "";
    static char input[MAX_MESSAGE_LENGTH + 1] = ""; // Buffer for incoming message
    unsigned int message_pos = 0;
    bool GotCommand = false;
    while (true) {
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
