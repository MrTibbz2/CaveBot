#include "CaveSense.h"
#include "config.h"
#include "pico/multicore.h"
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "tusb.h"
#include <iostream>
#include <optional>
#include <string>
#include <memory>
CaveSense::CaveSense() {
    init();
}

CaveSense::~CaveSense() {
    // Ensure scanning stops before destruction
    if (scanner && scanner->IsScanning()) {
        scanner->EndScan();
    }
}

void CaveSense::init() {
    // Initialize hardware
    stdio_init_all();
    
    // Setup LED pin for status indication
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    gpio_put(PICO_DEFAULT_LED_PIN, false);
    
    // Create scanner as shared_ptr
    scanner = std::make_shared<Scanner>();
}
Scanner::Scanner() {
    std::cout << "Initializing " << SENSOR_CONFIG.size() << " sensors..." << std::endl;
    for (const auto& config : SENSOR_CONFIG) {
        std::cout << "Creating sensor " << config.name << ": trigger=" << (int)config.triggerPin 
                  << ", echo=" << (int)config.echoPin << std::endl;
        Sensors.emplace_back(config.triggerPin, config.echoPin);
        Sensors.back().init();
        SensorNames.push_back(config.name);
    }
    std::cout << "Scanner initialization complete" << std::endl;
}
uart::uart() {
    // TinyUSB is initialized by stdio_init_all()
    buffer.reserve(64); // Pre-allocate buffer space for efficiency
}

// Static weak_ptr to current scanner instance for core1
static std::weak_ptr<Scanner> currentScannerWeak;

// Static function for core1 execution
static void core1_scan_task() {
    while (true) {
        auto scanner = currentScannerWeak.lock();
        if (!scanner) {
            sleep_ms(10);
            continue;
        }
        
        if (scanner->scanning.load()) {
            std::cout << "{\"sensor_data\": {";
            for (size_t i = 0; i < scanner->Sensors.size(); ++i) {
                if (i > 0) std::cout << ",";
                float distance = scanner->Sensors[i].measure_cm();
                std::cout << "\"" << scanner->SensorNames[i] << "\": " << distance;
            }
            std::cout << "}}" << std::endl;
            
            sleep_ms(100);
        } else {
            sleep_ms(10);
        }
    }
}

bool Scanner::BeginScan() {
    if (scanning.load()) {
        std::cout << "Scan already in progress." << std::endl;
        return false;
    }
    
    scanning.store(true);
    return true;
}



std::optional<std::string> uart::readBuffer(bool (*tud_cdc_connected)(), uint32_t (*tud_cdc_available)()) {
    if (!tud_cdc_connected()) {
        return std::nullopt; // No connection - return nullopt for consistency
    }
    
    while (tud_cdc_available()) {
        char ch = tud_cdc_read_char();
        
        // Handle command termination
        if (ch == '\n' || ch == '\r') {
            if (!buffer.empty()) {
                std::string command = buffer;
                buffer.clear();
                return command;
            }
            continue; // Skip empty lines
        }
        
        // Buffer overflow protection
        if (buffer.length() >= 32) {
            buffer.clear(); // Reset on overflow
            std::cout << "ERROR: Command too long" << std::endl;
            continue;
        }
        
        // Only accept printable ASCII characters
        if (ch >= 32 && ch <= 126) {
            buffer += ch;
        }
    }
    
    return std::nullopt; // No complete command yet
}
void uart::executeCommand(const std::string& command, Scanner& scanner, Status& currentStatus) {
    auto cmdOpt = from_string(command);
    if (!cmdOpt) {
        std::cout << "ERROR: Unknown command" << std::endl;
        return;
    }
    
    switch (*cmdOpt) {
        case Commands::ENDSCAN:
            if (scanner.EndScan()) {
                std::cout << "stopped scanner sucessfully." << std::endl;
                currentStatus = Status::IDLE;
            } else {
                std::cout << "ERROR: Stop failed" << std::endl;
                currentStatus = Status::FAULT;
            }
            break;
            
        case Commands::BEGINSCAN:
            if (scanner.BeginScan()) {
                // std::cout << "beggining scan." << std::endl; // adds garbled text to output
                currentStatus = Status::SCANNING;
            } else {
                std::cout << "ERROR: Start failed" << std::endl;
                currentStatus = Status::FAULT;
            }
            break;
            
        case Commands::GETSTATUS:
            if (currentStatus == Status::SCANNING) {
                std::cout << "{\"status\": \"SCANNING\"}" << std::endl;
            } else if (currentStatus == Status::IDLE) {
                std::cout << "{\"status\": \"IDLE\"}" << std::endl;
            } else if (currentStatus == Status::USB_WAITING) {
                std::cout << "{\"status\": \"USB_WAITING\"}" << std::endl;
            } else if (currentStatus == Status::FAULT) {
                std::cout << "{\"status\": \"FAULT\"}" << std::endl;
            } else {
                std::cout << "{\"status\": \"UNKNOWN\"}" << std::endl;
            }
            break;
    }
}


void CaveSense::main() {
    // Wait for USB connection before proceeding
    while (!tud_cdc_connected()) {
        currentStatus = Status::USB_WAITING;
        UpdateStatusLed();
        tud_task();
        sleep_ms(100);
    }
    
    currentStatus = Status::IDLE;
    std::cout << "CaveSense initialized - Ready for commands" << std::endl;
    
    // Launch persistent core1 task
    currentScannerWeak = scanner;
    multicore_launch_core1(core1_scan_task);
    
    // Main event loop
    while (true) {
        // Update status based on scanner state
        if (scanner && scanner->IsScanning()) {
            currentStatus = Status::SCANNING;
        } else if (currentStatus == Status::SCANNING) {
            // Transition from scanning to idle
            currentStatus = Status::IDLE;
        }
        
        // Handle USB disconnection
        if (!tud_cdc_connected() && currentStatus != Status::USB_WAITING) {
            // Stop scanning if USB disconnects
            if (scanner && scanner->IsScanning()) {
                scanner->EndScan();
            }
            currentStatus = Status::USB_WAITING;
        } else if (tud_cdc_connected() && currentStatus == Status::USB_WAITING) {
            currentStatus = Status::IDLE;
        }
        
        UpdateStatusLed();
        
        // Process incoming commands
        auto command = serial.readBuffer(tud_cdc_connected, tud_cdc_available);
        if (command && scanner) {
            serial.executeCommand(*command, *scanner, currentStatus);
        }
        
        // Service USB stack
        tud_task();
        sleep_ms(10); // Small delay to prevent busy waiting
    }
}

void CaveSense::UpdateStatusLed() {
    static uint64_t lastBlink = 0;
    static bool ledState = false;
    uint64_t now = time_us_64();
    
    switch (currentStatus) {
        case Status::USB_WAITING:
            // LED off - waiting for USB connection
            gpio_put(PICO_DEFAULT_LED_PIN, false);
            break;
            
        case Status::IDLE:
            // LED solid on - ready for commands
            gpio_put(PICO_DEFAULT_LED_PIN, true);
            break;
            
        case Status::SCANNING:
            // LED slow blink - scanning in progress
            if (now - lastBlink > 500000) { // 500ms intervals
                ledState = !ledState;
                gpio_put(PICO_DEFAULT_LED_PIN, ledState);
                lastBlink = now;
            }
            break;
            
        case Status::FAULT:
            // LED fast blink - error condition
            if (now - lastBlink > 100000) { // 100ms intervals
                ledState = !ledState;
                gpio_put(PICO_DEFAULT_LED_PIN, ledState);
                lastBlink = now;
            }
            break;
    }
}