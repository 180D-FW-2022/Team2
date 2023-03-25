This code will test the delivery of motor commands through Bluetooth
communications. It uses simple keyboard commands to control the motors.
Use "q" and "a" to control the left motor and "o" and "l" to control the
right motors. As of now, the Pi will only print out whatever command is
inputted.

1. In "bluetoothMotorUserSide.py", replace the argument in the
   variable "bd_addr" with the bluetooth MAC address of your raspberry
   pi
2. Run "bluetoothMotorPiSide.py" on the raspberry pi
3. Run "bluetoothMotorUserSide.py" on the UI
4. Instructions will print out on the screen for keyboard input. Use
   those instructions to send motor commands to the pi