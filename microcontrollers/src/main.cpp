#include <stdio.h>
#include "pico/stdlib.h"
#include <tusb.h>
#define MAX_MESSAGE_LENGTH 12
int main()
{
stdio_init_all();
while (!tud_cdc_connected())
{
sleep_ms(100);
}
printf("tud_cdc_connected()\n");
while (true)
{
//Check to see if anything is available in the serial receive buffer
while (tud_cdc_available())
{
//Create a place to hold the incoming message
static char message[MAX_MESSAGE_LENGTH];
static unsigned int message_pos = 0;
//Read the next available byte in the serial receive buffer
char inByte = getchar();
//Message coming in (check not terminating character) and guard for over message size
if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
{
//Add the incoming byte to our message
message[message_pos] = inByte;
message_pos++;
}
//Full message received...
else
{
//Add null character to string
message[message_pos] = '\0';
printf("%s\n",message);
//Reset for the next message
message_pos = 0;
}
}
}

return 0;
}