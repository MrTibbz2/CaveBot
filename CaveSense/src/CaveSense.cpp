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
    
    // Launch persistent core1 task
    currentScannerWeak = scanner;
    multicore_launch_core1(core1_scan_task);
}
Scanner::Scanner() {
    std::cout << "Initializing " << SENSOR_CONFIG.size() << " sensors..." << std::endl;
    for (const auto& config : SENSOR_CONFIG) {
        std::cout << "Creating sensor: trigger=" << (int)config.triggerPin 
                  << ", echo=" << (int)config.echoPin 
                  << ", pio=" << (config.pio == pio0 ? "pio0" : "pio1")
                  << ", sm=" << config.sm << std::endl;
        Sensors.emplace_back(config.pio, config.sm, config.triggerPin);
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
    std::cout << "Core1 scan task started" << std::endl;
    
    while (true) {
        auto scanner = currentScannerWeak.lock(); // Safe access
        if (!scanner) {
            std::cout << "Scanner destroyed, core1 exiting" << std::endl;
            return; // Scanner destroyed, exit
        }
        
        if (scanner->stopRequested.load()) {
            std::cout << "Stop requested, core1 exiting" << std::endl;
            break;
        }
        
        std::cout << "Scanning " << scanner->Sensors.size() << " sensors..." << std::endl;
        
        for (auto& sensor : scanner->Sensors) {
            if (scanner->stopRequested.load()) break;
            
            sensor.TriggerRead();
            
            // Wait for sensor to complete
            while (sensor.is_sensing && !scanner->stopRequested.load()) {
                sleep_us(100);
            }
            
            if (!scanner->stopRequested.load()) {
                std::cout << "Sensor reading: " << sensor.distance << " cm" << std::endl;
            }
        }
        
        // Delay between scan cycles
        sleep_ms(100);
    }
    
    std::cout << "Core1 scan task ending" << std::endl;
    
    // Safe final access
    if (auto scanner = currentScannerWeak.lock()) {
        scanner->scanning.store(false);
    }
}

bool Scanner::BeginScan() {
    if (scanning.load()) {
        std::cout << "Scan already in progress." << std::endl;
        return false;
    }
    
    stopRequested.store(false);
    scanning.store(true);
    currentScannerWeak = shared_from_this();
    
    multicore_launch_core1(core1_scan_task);
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
            std::cout << "STATUS:" << static_cast<int>(currentStatus) << std::endl;
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