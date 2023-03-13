ServoMotorTestNotes:

This document details the GPIO PWM controls used in the python programs of this folder. It notes the value ranges of the motors used to initial calibration.

Basic_Control.py:

This is a calibration program used to test a range of duty cycle values. This experimentation allows the vehicle to move evenly by equalizing the RPM of the movement motors in each vehicle.

TestRun.py:

This program is used to compare the relative speeds of each individually calibrated movement. This determines if turning left is faster or slower than turning right and if the device moves as expected with different combinations of movements.

Bluetooth_Control_Test.py:

This program is a frozen state of Basic_Control so that a stable python program exists with the necessary GPIO commands which can be modified for bluetooth controls.
