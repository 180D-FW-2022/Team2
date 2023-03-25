Note: This is just to test the delivery of gesture recognition commands
through Bluetooth. We have updated the gesture recognition code to
detect markers instead of colors for better reliability and less false
detections.

1. In "BluetoothGestureUser.py", replace the argument in the
   variable "bd_addr" with the bluetooth MAC address of your raspberry
   pi
2. Run "bluetoothMotorPiSide.py" from the "Bluetooth Motor Control"
   folder on the raspberry pi
3. Run "BluetoothGestureUser.py" on the UI
4. A live video feed will stream on the UI. Hold up a blue object to
   the screen to send motor commands to the pi. The screen is
   partitioned into four parts. The upper left part corresponds to
   forward movement with the left motor, while the lower left part
   corresponds to backwards movement with the left motor. The upper
   right and lower right parts of the screen does the same for the
   right motor.