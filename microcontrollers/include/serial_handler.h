#pragma once
#include <array>
class status;
class commands;

class status {
public:
    struct SystemState {
        bool isConnected = false;
        bool readyForCommands = false;
        bool systemHealthy = false;
        char lastError[17] = "";
        char lastCommand[17] = "";


    };
    SystemState currentState;
};

class commands {
    struct Command {
        char commandCall[17] = "";
        

    };

};