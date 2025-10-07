#include <atomic>
#include <array>
#include <optional>
#include <vector>
#include <string>
#include <iostream>
#include <memory>
#include "hcsr04.h"
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
    bool BeginScan();
    bool EndScan() {
        if (!scanning.load()) {
            return true;
        }
        scanning.store(false);
        return true;
    };
    bool IsScanning() { return scanning.load(); };
    
    std::vector<HCSR04> Sensors;
    std::vector<std::string> SensorNames;
    std::atomic<bool> scanning{false};
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