#include <atomic>
#include <array>
#include <optional>
#include <vector>
#include <string>
#include <iostream>
#include <memory>
#include "distance_sensor.h"
#include "pico/time.h"


enum class Commands {
    ENDSCAN,
    BEGINSCAN,
    GETSTATUS,
    COUNT
};

// Array of corresponding strings
constexpr std::array<std::string_view, static_cast<size_t>(Commands::COUNT)> CommandStrings = {
    "ENDSCAN",
    "BEGINSCAN",
    "GETSTATUS"
};

constexpr std::optional<Commands> from_string(std::string_view str) {
    for (size_t i = 0; i < static_cast<size_t>(Commands::COUNT); ++i) {
        if (CommandStrings[i] == str) {
            return static_cast<Commands>(i);  // Return the enum value
        }
    }
    return std::nullopt;  // Return nullopt if no match is found
}

// Forward declaration
class Scanner;

enum class Status { // status of the system. returned by GETSTATUS command, shown by led.
    USB_WAITING, // light off. means system is waiting for usb connection.
    IDLE, // light solid.
    SCANNING, // light flashing
    FAULT // light flashing fast
};

class uart {
public:
    uart();
    std::optional<std::string> readBuffer(bool (*tud_cdc_connected)(), uint32_t (*tud_cdc_available)());
    void executeCommand(const std::string& command, Scanner& scanner, Status& currentStatus); 
    // simple commands only, no modularity needed.
    // if command is status/stopscan, run on core0. if command is begin scan, run on core1.
private:
    std::string buffer;
};
class Scanner : public std::enable_shared_from_this<Scanner> {
public:
    Scanner();
    bool BeginScan(); // creates the core1 task and begins scanning, outputting to logs
    bool EndScan() {
        if (!scanning.load()) {
            return true; // Already stopped
        }
        
        stopRequested.store(true);
        uint64_t stopRequestedTime = time_us_64();
        
        // Wait for graceful shutdown
        while (scanning.load()) {
            if (time_us_64() - stopRequestedTime > 5000000) { // 5 second timeout
                std::cout << "Timeout waiting for core1 to stop." << std::endl;
                return false; // Timeout - scan didn't stop gracefully
            }
            sleep_ms(10);
        }
        return true;
    };  // set flag. waits for timeout of core1 to end otherwise fails.
    bool IsScanning() { return scanning.load(); }; // returns true if currently scanning
    
    // Public access for static core1 function
    std::vector<DistanceSensor> Sensors;
    std::atomic<bool> scanning{false};
    std::atomic<bool> stopRequested{false};
private:
        
};

class CaveSense {
public:

    Status getStatus() { return currentStatus; };
    CaveSense();
    ~CaveSense();
     // initializes the system, setting up serial and scanner and beginning serial read loop.
    void main();
    void UpdateStatusLed(); // updates the status led based on current status.
private:
    void init();
    std::shared_ptr<Scanner> scanner;
    uart serial;
    Status currentStatus{Status::USB_WAITING};
    
};