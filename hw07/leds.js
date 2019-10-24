#!/usr/bin/env node
// Blinks various LEDs
const Blynk = require('blynk-library');
const b = require('bonescript');
const util = require('util');

const LED0 = 'USR3';
const button = 'P9_25';
//initialized pwm pin
const LED1 = 'P9_14';
b.pinMode(LED1, b.OUTPUT);
b.pinMode(LED0, b.OUTPUT);
b.pinMode(button, b.INPUT);

const AUTH = 'HCz1k1mX2LrZ-r_T7RZP02REJGktKfSS';


var blynk = new Blynk.Blynk(AUTH);

var v0 = new blynk.VirtualPin(0);
var v10 = new blynk.WidgetLED(10);
//initialized new virtual pin and used it to control pwm pin
var v5 = new blynk.VirtualPin(5);
v5.on('write', function(param){
     console.log('v5:', param[0]);
     b.analogWrite(LED1, param[0]/1023);
});
v0.on('write', function(param) {
    console.log('V0:', param[0]);
    b.digitalWrite(LED0, param[0]);
});

v10.setValue(0);    // Initiallly off

b.attachInterrupt(button, toggle, b.CHANGE);

function toggle(x) {
    console.log("V10: ", x.value);
    x.value ? v10.turnOff() : v10.turnOn();
}
