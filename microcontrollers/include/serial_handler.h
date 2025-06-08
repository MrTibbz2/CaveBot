#pragma once


#include <cstdio> // For snprintf, printf
#include <cstring> // For strcmp, strlen

// Max buffer size for outgoing serial message. Adjust as needed.
#define MAX_OUTPUT_BUFFER_SIZE 512


// Top-level identifier for the log message.
enum class LogIdentifier {
    CORE1,
    COMMAND,
    INFO,
    ERROR,
    UNKNOWN
};

// Status codes within the JSON payload.
enum class LogStatus {
    SUCCESS,
    FAILURE,
    THREAD_STARTED,
    THREAD_STOPPED,
    THREAD_LOCKED,
    NO_THREAD_RUNNING,
    READY,
    ACTIVE,
    IDLE,
    INVALID_COMMAND,
    BUFFER_OVERFLOW,
    SENSOR_FAULT,
    UNKNOWN_STATUS,
    UNHEALTHY,
    INITIALISING,
};

// Helper to convert LogIdentifier enum to string.
const char* getIdentifierString(LogIdentifier id);

// Helper to convert LogStatus enum to string.
const char* getStatusString(LogStatus status);

class output {
public:
    // Structured data for a log entry.
    struct outdata {
        LogIdentifier identifier;       // Top-level message category (e.g., Core1, INFO)
        const char* message_type;       // Internal JSON "type" field (e.g., "data_stream", "system_status")
        LogStatus status_code;          // Internal JSON "status" field (e.g., "success", "thread_locked")
        const char* payload_json = nullptr; // Optional: JSON string for the "payload" key.
    };

    // Formats and sends log data over serial.
    static int logData(output::outdata data);

    output() = default; // Default constructor
    void get_string_until_delimiter(char* dest, const char* source, char delimiter, size_t dest_size);

};


class status;
class commands;




class status {
public:
    struct SystemState {
        bool isConnected = false;
        bool initialised = false;
        bool readyForCommand = false;
        bool systemHealthy = true;
        char Core1Status[17] = "";

        


    };
    struct Core1Status {
        bool isRunning = false;
        char statusMessage[17] = "";
    };
    static SystemState currentState;
    static Core1Status currentCore1State; 
};

class commands {
public:
    struct Command {
        char commandCall[17] = "";
        char name[17] = "";
        int (*execution)(void);
        
        

    };
    Command getState;
    Command InitAll;
    commands(); // Constructor declaration
    commands::Command checkCommand(char* command);
    int ExecuteCommand(commands::Command command);

    Command ExecutableCommands[2] = {
        getState,
        InitAll

    };
    int init();
    char* ReadBuffer(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()); 

};
