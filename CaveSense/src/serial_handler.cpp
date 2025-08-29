// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

#include "serial_handler.h"
#include <cstring>
#include <stdio.h>
#include "pico/multicore.h"
#include <cctype>
#include "pico/stdlib.h"
#include <tusb.h>
#include "distance_sensor.h"
#define SENSORCOUNT 1
static const int SENSORPINS[SENSORCOUNT] = { 0 }; // sensor pins array



// Private static variables for encapsulated state
status::SystemState status::currentState;
status::Core1Status status::currentCore1State;
// Getters
status::SystemState status::getCurrentState() { return currentState; }
status::Core1Status status::getCurrentCore1State() { return currentCore1State; }
// Setters
void status::setConnected(bool val) { currentState.isConnected = val; }
void status::setInitialised(bool val) { currentState.initialised = val; }
void status::setReadyForCommand(bool val) { currentState.readyForCommand = val; }
void status::setSystemHealthy(bool val) { currentState.systemHealthy = val; }
void status::setCore1Running(bool val) { currentCore1State.isRunning = val; }
void status::setCore1StatusMessage(const char* msg) {
    std::strncpy(currentCore1State.statusMessage, msg, MAX_STATUS_MSG_LENGTH);
    currentCore1State.statusMessage[MAX_STATUS_MSG_LENGTH] = '\0';
}

// function implementations

void output::get_string_until_delimiter(char* dest, const char* source, char delimiter, size_t dest_size) const {
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
    char status_payload_buffer[128];
    status::SystemState state = status::getCurrentState(); // Use getter for encapsulation
    int payload_len = snprintf(status_payload_buffer, sizeof(status_payload_buffer),
                                "{ "
                                    "\"is_connected\": %s, "
                                    "\"initialised\": %s, "
                                    "\"ready_for_command\": %s, "
                                    "\"system_healthy\": \"%s\""
                                " }",
                               state.isConnected ? "true" : "false",
                               state.initialised ? "true" : "false",
                               state.readyForCommand ? "true" : "false",
                               state.systemHealthy ? "true" : "false"
                              );
    output::outdata status_log_data;
    if (state.initialised && state.readyForCommand && state.systemHealthy) {
        status_log_data.status_code = LogStatus::READY;
    } else if (!state.systemHealthy) {
        status_log_data.status_code = LogStatus::UNHEALTHY;
    } else if (state.systemHealthy) {
        status_log_data.status_code = LogStatus::INITIALISING;
    }
    status_log_data.identifier = LogIdentifier::INFO;
    status_log_data.message_type = "system_status";
    status_log_data.payload_json = status_payload_buffer;
    output::logData(status_log_data);
    return 0;
}

int executeInitAll() {

    return 0;
}
int executeBeginScan() {
    sensor sensorInstance;
    sensorInstance.BeginSensorRead(SENSORCOUNT, SENSORPINS);
    output::logData({
        LogIdentifier::COMMAND,
        "exec_result",
        LogStatus::SUCCESS,
    });
    return 0;
}
int executeEndScan() {
    // Placeholder for actual end scan logic
    status::setCore1StopRequested(true); // Set stop requested to true
    int mssinceon = to_ms_since_boot(get_absolute_time());
    while (status::getCurrentCore1State().isRunning == true) {
        // Wait for the core to stop
        if ((to_ms_since_boot(get_absolute_time()) - mssinceon) > 10000) {
            output::logData({
                LogIdentifier::COMMAND,
                "core1_status",
                LogStatus::THREAD_LOCKED,
                "{\"error\": \"core1_stop_timeout\"}"
            });
            return 1; 

        }
        sleep_ms(100);

    }
    status::setCore1StopRequested(false); // Reset stop requested
    output::logData({
        LogIdentifier::COMMAND,
        "core1_status",
        LogStatus::THREAD_STOPPED
    });
    return 0;

}
// Constructor or initialization function for commands
commands::commands() {
    // Set up getState command
    std::strncpy(getState.commandCall, "GETSTATE", MAX_COMMAND_LENGTH);
    getState.commandCall[MAX_COMMAND_LENGTH] = '\0'; // Ensure null-termination
    std::strncpy(getState.name, "Get State", MAX_COMMAND_LENGTH);
    getState.name[MAX_COMMAND_LENGTH] = '\0';
    getState.execution = &executeGetState;

    // Set up InitAll command
    std::strncpy(InitAll.commandCall, "INITALL", MAX_COMMAND_LENGTH);
    InitAll.commandCall[MAX_COMMAND_LENGTH] = '\0';
    std::strncpy(InitAll.name, "Initialize All", MAX_COMMAND_LENGTH);
    InitAll.name[MAX_COMMAND_LENGTH] = '\0';
    InitAll.execution = &executeInitAll;


    // Set up BeginScan command
    std::strncpy(BeginScan.commandCall, "BEGINSCAN", MAX_COMMAND_LENGTH);
    BeginScan.commandCall[MAX_COMMAND_LENGTH] = '\0';
    std::strncpy(BeginScan.name, "Begin Scan", MAX_COMMAND_LENGTH);
    BeginScan.name[MAX_COMMAND_LENGTH] = '\0';
    BeginScan.execution = &executeBeginScan; // TODO
    // Set up EndScan command
    std::strncpy(EndScan.commandCall, "ENDSCAN", MAX_COMMAND_LENGTH);

    EndScan.commandCall[MAX_COMMAND_LENGTH] = '\0';
    std::strncpy(EndScan.name, "End Scan", MAX_COMMAND_LENGTH);
    EndScan.name[MAX_COMMAND_LENGTH] = '\0';
    EndScan.execution = &executeEndScan; // TODO
    // Update ExecutableCommands array
    ExecutableCommands[0] = getState;
    ExecutableCommands[1] = InitAll;
    ExecutableCommands[2] = BeginScan;
    ExecutableCommands[3] = EndScan; 
}
commands::Command commands::checkCommand(const char* command) { // Use const for input
    for (int i = 0; i < sizeof(ExecutableCommands) / sizeof(ExecutableCommands[0]); i++) {
        if (std::strncmp(command, ExecutableCommands[i].commandCall, MAX_COMMAND_LENGTH) == 0) {
            return ExecutableCommands[i];
        }
    }
    commands::Command nullcmd;
    std::strncpy(nullcmd.name, "NULL", MAX_COMMAND_LENGTH);
    nullcmd.name[MAX_COMMAND_LENGTH] = '\0';
    return nullcmd;
}
int commands::ExecuteCommand(const commands::Command& command) { // Pass by const ref
    if (command.execution != nullptr) {
        return command.execution();
    } else {
        if (std::strncmp(command.name, "NULL", MAX_COMMAND_LENGTH) == 0) {
            printf("unknown command\n");
        }
        return 1;
    }
}
char* commands::ReadBuffer(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()) const {
    if (!status::getCurrentState().initialised) { // Use getter for encapsulation
        static char error_ret[6] = "error";
        return error_ret;
    }
    static char input[MAX_MESSAGE_LENGTH + 1] = {0};
    unsigned int message_pos = 0;
    bool GotCommand = false;
    while (true) {
        while (!GotCommand) {
            while (tud_cdc_available()) {
                char inByte = getchar();
                if (inByte != '\n' && message_pos < MAX_MESSAGE_LENGTH) {
                    input[message_pos++] = inByte;
                } else {
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
