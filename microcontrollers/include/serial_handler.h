#pragma once


#include <cstdio> // For snprintf, printf
#include <cstring> // For strcmp, strlen

// Max buffer size for outgoing serial message. Adjust as needed.
constexpr size_t MAX_OUTPUT_BUFFER_SIZE = 512; // Changed from #define for type safety
constexpr size_t MAX_COMMAND_LENGTH = 16;     // Added for commandCall and name buffers
constexpr size_t MAX_STATUS_MSG_LENGTH = 16;  // Added for statusMessage buffer
constexpr size_t MAX_MESSAGE_LENGTH = 24;     // Added for message buffer in ReadBuffer

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
    static int logData(const output::outdata& data); // Pass by const reference for safety

    // Error logging helper: logs function, line, and optional address over USB
    static void logFirmwareError(const char* func, int line, const void* addr = nullptr) {
        char msg[128];
        snprintf(msg, sizeof(msg), "FIRMWARE ERROR in %s at line %d, addr: 0x%p", func, line, addr);
        logData({LogIdentifier::ERROR, "firmware_fault", LogStatus::FAILURE, msg});
    }

    output() = default; // Default constructor
    void get_string_until_delimiter(char* dest, const char* source, char delimiter, size_t dest_size) const; // Mark as const
private:
    // No public data members: encapsulation
};


class status;
class commands;


class sensor;
class sensor {
public:
    
    int BeginSensorRead(int sensorcount, int* sensorpins);
};

class status {
public:
    struct SystemState {
        bool isConnected = false;
        bool initialised = false;
        bool readyForCommand = false;
        bool systemHealthy = true;

    };
    struct Core1Status {
        bool isRunning = false;
        char statusMessage[MAX_STATUS_MSG_LENGTH + 1] = {0};
        volatile bool core1_stop_requested = false;
        //volatile = the compiler does it without optimisations and to read actual position, safer.
    };
    // Getters
    static SystemState getCurrentState();
    static Core1Status getCurrentCore1State();
    // Setters
    static void setConnected(bool val);
    static void setInitialised(bool val);
    static void setReadyForCommand(bool val);
    static void setSystemHealthy(bool val);
    static void setCore1Running(bool val);
    static void setCore1StatusMessage(const char* msg);
    static void setCore1StopRequested(bool val) {
        currentCore1State.core1_stop_requested = val;
    }
    static bool isCore1StopRequested() {
        return currentCore1State.core1_stop_requested;
    }
private:
    static SystemState currentState;
    static Core1Status currentCore1State;
};

class commands {
public:
    struct Command {
        char commandCall[MAX_COMMAND_LENGTH + 1] = {0}; // Use constexpr and zero-init
        char name[MAX_COMMAND_LENGTH + 1] = {0};        // Use constexpr and zero-init
        int (*execution)(void);
    };
    Command getState;
    Command InitAll;
    commands(); // Constructor declaration
    commands::Command checkCommand(const char* command); // Use const for input
    int ExecuteCommand(const commands::Command& command); // Pass by const ref

    Command ExecutableCommands[2] = {
        getState,
        InitAll
    };
    int init();
    char* ReadBuffer(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()) const; // Mark as const
};
