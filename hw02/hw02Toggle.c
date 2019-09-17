////////////////////////////////////////
//	blinkLED.c
//      Blinks the USR3 LED.
//	Wiring:	None
//	Setup:	
//	See:	
////////////////////////////////////////
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <libsoc_gpio.h>
#include <libsoc_debug.h>

#define GPIO_OUTPUT 50


int main(void) {
    gpio *gpio_output;   //create gpio pointer
    libsoc_set_debug(1); //Enable debug output
    
    //Request gpio
    gpio_output = libsoc_gpio_request(GPIO_OUTPUT, LS_SHARED);
    
    //set direction to OUTPUT
    libsoc_gpio_set_direction(gpio_output, OUTPUT);
    libsoc_set_debug(0);  //Turn off debug printing for fast toggle
    
    int i;
    for(i=0; i<1000000; i++) { //toggle GPIO
        libsoc_gpio_set_level(gpio_output, HIGH);
        usleep(100000); //sleep 100000us
        libsoc_gpio_set_level(gpio_output, LOW);
        usleep(100000);
    }
    
    if (gpio_output){
        //Free gpio request memory
        libsoc_gpio_free(gpio_output);
    }
    
    return EXIT_SUCCESS;
}