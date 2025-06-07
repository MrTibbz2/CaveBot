#include <stdio.h>
#include "pico/stdlib.h"
#include <tusb.h>

#define MAX_MESSAGE_LENGTH 16

int main() {
    stdio_init_all();  // Initialize USB serial I/O

    // Wait for USB connection
    while (!tud_cdc_connected()) {
        sleep_ms(100);
    }
    printf("USB connected!\n");

    char input[MAX_MESSAGE_LENGTH + 1]; // Buffer for incoming message
    unsigned int message_pos = 0; // Tracks the position in the buffer

    while (true) {
        // Check if there is data available in the USB serial buffer
        while (tud_cdc_available()) {
            char inByte = getchar();  // Read one character at a time

            // Add the character to the buffer unless it's a newline
            if (inByte != '\n' && message_pos < MAX_MESSAGE_LENGTH) {
                input[message_pos++] = inByte;
            } else { 
                // Null-terminate and print when a newline is received
                input[message_pos] = '\0';
                printf("Your message is: %s\n", input);
                message_pos = 0;  // Reset buffer for next message
            }
        }
    }

    return 0;
}