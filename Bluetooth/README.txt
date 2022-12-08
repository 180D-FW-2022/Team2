This folder contains the contents of the Bluetooth developement of our project.
The demo of the project can be run through scripts in this folder and its
subfolders.

Before starting any scripts, ensure that the raspberry pi is connected via
bluetooth to the laptop you want to use as the user interface (UI).

Start with "Bluetooth Basic Connectivity Test"
	1. Run "bluetoothTestReceiver.py" on the raspberry pi
	2. In "bluetoothTestSender.py", replace the argument in the variable
	   "bd_addr" with the bluetooth MAC address of your raspberry pi
	3. Run "bluetoothTestSender.py" on the UI
	4. You should see the "Hello from Surfacde Laptop!" print statement
	   on the pi's terminal every 2 seconds.

Move on to "Bluetooth Motor Control"
	1. In "bluetoothMotorUserSide.py", replace the argument in the
	   variable "bd_addr" with the bluetooth MAC address of your raspberry
	   pi
	2. Run "bluetoothMotorPiSide.py" on the raspberry pi
	3. Run "bluetoothMotorUserSide.py" on the UI
	4. Instructions will print out on the screen for keyboard input. Use
	   those instructions to send motor commands to the pi

Go to "Bluetooth Gesture Recognition"
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

The folder "Bluetooth Video Streaming" is not yet developed and was not a part
of the demo.