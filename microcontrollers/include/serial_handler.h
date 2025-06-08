#pragma once

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
        char lastError[17] = "none";
        char lastCommand[17] = "";


    };
    struct Core1Status {
        bool isRunning = false;
        char statusMessage[17] = "";
    };
    static SystemState currentState;
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
    commands::Command checkCommands(char* command);
    int ExecuteCommand(commands::Command command);

    Command ExecutableCommands[2] = {
        getState,
        InitAll

    };
    int init();
    char* ReadBufferuntilCommand(bool (*tud_cdc_connected)(), unsigned long (*tud_cdc_available)()); 

};
