// From : http://stackoverflow.com/questions/13124271/driving-beaglebone-gpio-through-dev-mem
//
// Read one gpio pin and write it out to another using mmap.
// Be sure to set -O3 when compiling.
// Modified by Mark A. Yoder  26-Sept-2013
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h> 
#include <signal.h>    // Defines signal-handling functions (i.e. trap Ctrl-C)
#include "beaglebone_gpio.h"

/****************************************************************
 * Global variables
 ****************************************************************/
int keepgoing = 1;    // Set to 0 when ctrl-c is pressed

/****************************************************************
 * signal_handler
 ****************************************************************/
void signal_handler(int sig);
// Callback called when SIGINT is sent to the process (Ctrl-C)
void signal_handler(int sig)
{
    printf( "\nCtrl-C pressed, cleaning up and exiting...\n" );
	keepgoing = 0;
}

int main(int argc, char *argv[]) {
    volatile void *gpio_addr;
    volatile void *gpio_addr2;
    volatile unsigned int *gpio_oe_addr;
    volatile unsigned int *gpio_oe_addr2;
    volatile unsigned int *gpio_datain;
    volatile unsigned int *gpio_datain2;
    volatile unsigned int *gpio_setdataout_addr2;
    volatile unsigned int *gpio_setdataout_addr;
    volatile unsigned int *gpio_cleardataout_addr;
    volatile unsigned int *gpio_cleardataout_addr2;
    unsigned int reg;
    unsigned int reg2;

    // Set the signal callback for Ctrl-C
    signal(SIGINT, signal_handler);

    int fd = open("/dev/mem", O_RDWR);
    
    system("config-pin P9_11 gpio");
    
    gpio_addr = mmap(0, GPIO0_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO0_START_ADDR);

    gpio_oe_addr           = gpio_addr + GPIO_OE;
    gpio_datain            = gpio_addr + GPIO_DATAIN;
    gpio_setdataout_addr   = gpio_addr + GPIO_SETDATAOUT;
    gpio_cleardataout_addr = gpio_addr + GPIO_CLEARDATAOUT;

    if(gpio_addr == MAP_FAILED) {
        printf("Unable to map ADDR1\n");
        exit(1);
    }
    
    gpio_addr2 = mmap(0, GPIO1_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 
                        GPIO1_START_ADDR);

    gpio_oe_addr2           = gpio_addr2 + GPIO_OE;
    gpio_datain2            = gpio_addr2 + GPIO_DATAIN;
    gpio_setdataout_addr2   = gpio_addr2 + GPIO_SETDATAOUT;
    gpio_cleardataout_addr2 = gpio_addr2 + GPIO_CLEARDATAOUT;

    if(gpio_addr == MAP_FAILED) {
        printf("Unable to map ADDR2\n");
        exit(1);
    }
    
    reg = *gpio_oe_addr2;
    reg &= ~USR3;
    *gpio_oe_addr2 = reg;
    
    reg2 = *gpio_oe_addr2;
    reg2 &= ~USR1;
    *gpio_oe_addr2 = reg2;
    


    while(keepgoing) {
    	if(*gpio_datain & GPIO_07) {
    	    printf("Button works");
            *gpio_setdataout_addr= USR3;
    	} else {
            *gpio_setdataout_addr = USR3;
    	}
    	
     	if(*gpio_datain & GPIO_30) {
             *gpio_setdataout_addr= USR1;
     	} else {
             *gpio_cleardataout_addr = USR1;
    	}
        usleep(1500);
    }

    munmap((void *)gpio_addr, GPIO0_SIZE);
    munmap((void *)gpio_addr2, GPIO1_SIZE);
    close(fd);
    return 0;
}