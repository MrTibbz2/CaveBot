#pragma once
#include "pico/stdlib.h"
#include <cstdint>
#include <stdio.h>

class HCSR04 {
public:
    // Constructor: trigger and echo pins, optional timeout in microseconds
    HCSR04(uint trig_pin, uint echo_pin, uint32_t timeout_us = 30000)
        : trig_pin_(trig_pin), echo_pin_(echo_pin), timeout_us_(timeout_us) {}

    // Initialize GPIO pins (call once in main)
    void init() {
        gpio_init(trig_pin_);
        gpio_set_dir(trig_pin_, GPIO_OUT);
        gpio_put(trig_pin_, 0);

        gpio_init(echo_pin_);
        gpio_set_dir(echo_pin_, GPIO_IN);
        gpio_pull_down(echo_pin_);
    }

    // Measure distance in centimeters
    // Returns -1.0 if timeout/error
    float measure_cm() {
        // Send 10us trigger pulse
        gpio_put(trig_pin_, 1);
        sleep_us(10);
        gpio_put(trig_pin_, 0);

        // Wait for echo to go high
        uint32_t start_wait = time_us_32();
        while (!gpio_get(echo_pin_)) {
            if (time_us_32() - start_wait > timeout_us_) return -1.0f;
        }

        // Echo started
        uint32_t t0 = time_us_32();

        // Wait for echo to go low
        while (gpio_get(echo_pin_)) {
            if (time_us_32() - t0 > timeout_us_) return -1.0f;
        }
        uint32_t t1 = time_us_32();

        uint32_t pulse_us = t1 - t0;
        float distance_cm = (pulse_us * 0.0343f) / 2.0f; // speed of sound
        return distance_cm;
    }

private:
    uint trig_pin_;
    uint echo_pin_;
    uint32_t timeout_us_;
};
