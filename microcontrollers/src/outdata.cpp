#include "serial_handler.h"



// Converts LogIdentifier enum to its string representation.
const char* getIdentifierString(LogIdentifier id) {
    switch (id) {
        case LogIdentifier::CORE1: return "Core1";
        
        case LogIdentifier::COMMAND: return "Command";
        case LogIdentifier::INFO: return "INFO";
        case LogIdentifier::ERROR: return "ERROR";
        default: return "UNKNOWN_IDENTIFIER";
    }
}

// Converts LogStatus enum to its string representation.
const char* getStatusString(LogStatus status) {
    switch (status) {
        case LogStatus::SUCCESS: return "success";
        case LogStatus::FAILURE: return "failure";
        case LogStatus::THREAD_STARTED: return "thread_started";
        case LogStatus::THREAD_STOPPED: return "thread_stopped";
        case LogStatus::THREAD_LOCKED: return "thread_locked";
        case LogStatus::NO_THREAD_RUNNING: return "no_thread_running";
        case LogStatus::READY: return "ready";
        case LogStatus::ACTIVE: return "active";
        case LogStatus::IDLE: return "idle";
        case LogStatus::INVALID_COMMAND: return "invalid_command";
        case LogStatus::BUFFER_OVERFLOW: return "log_buffer_overflow";
        case LogStatus::SENSOR_FAULT: return "sensor_fault";
        case LogStatus::INITIALISING: return "initialising";
        case LogStatus::UNHEALTHY: return "unhealthy";
        default: return "unknown_status";
    }
}

int output::logData(const output::outdata& data) {
    status::SystemState state = status::getCurrentState();
    if (!state.initialised || !state.isConnected) { return 1; }

    char outputBuffer[MAX_OUTPUT_BUFFER_SIZE];
    int bytesWritten = 0;

    const char* idStr = getIdentifierString(data.identifier);
    const char* statusStr = getStatusString(data.status_code);

    // Construct the JSON-like string, including payload if present.
    if (data.payload_json != nullptr && data.payload_json[0] != '\0') {
        bytesWritten = snprintf(outputBuffer, MAX_OUTPUT_BUFFER_SIZE,
                                "%s: { \"type\": \"%s\", \"status\": \"%s\", \"payload\": %s }",
                                idStr, data.message_type, statusStr, data.payload_json);
    } else {
        bytesWritten = snprintf(outputBuffer, MAX_OUTPUT_BUFFER_SIZE,
                                "%s: { \"type\": \"%s\", \"status\": \"%s\" }",
                                idStr, data.message_type, statusStr);
    }

    // Handle buffer overflow during formatting.
    if (bytesWritten < 0 || bytesWritten >= MAX_OUTPUT_BUFFER_SIZE) {
        printf("ERROR: { \"type\": \"system\", \"status\": \"%s\", \"source_identifier\": \"%s\" }\n",
               getStatusString(LogStatus::BUFFER_OVERFLOW), idStr);
        return -1;
    }

    // Send formatted string via printf (Pico SDK typically routes this to UART).
    printf("%s\n", outputBuffer);

    return 0;
}