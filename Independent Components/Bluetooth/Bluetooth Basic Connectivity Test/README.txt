This is a test that should be ran to ensure that your laptop can communicate
to your Raspberry Pi via Bluetooth. It sends a very simple string object from
the laptop to the Pi.

Refer to "bluetooth_setup.txt" if you need help connecting the Pi to the
laptop or have trouble installing PyBluez.

1. Run "bluetoothTestReceiver.py" on the raspberry pi
2. In "bluetoothTestSender.py", replace the argument in the variable
   "bd_addr" with the bluetooth MAC address of your raspberry pi
3. Run "bluetoothTestSender.py" on the UI
4. You should see the "Hello from Surface Laptop!" print statement
	   on the pi's terminal every 2 seconds.