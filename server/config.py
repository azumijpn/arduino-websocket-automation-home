# Socket configuration

# Network interface
socketBind = "0.0.0.0"
socketPort = 8000

# Serial interface
# example for one serial port : portCom = [{ 'port' : '/dev/ttyUSB0', 'baudrate': 115200 }]
# example for n serial port : portCom = [{ 'port': '/dev/ttyUSB0', 'baudrate': 115200 }, { 'port':'/dev/ttyUSB1', 'baudrate': 115200 }]
# example for n serial port for windows: portCom = [{ 'port': 'COM1', 'baudrate': 115200 }, {'port': 'COM2', 'baudrate': 115200 }]
portCom = [{ 'port' : '/dev/ttyUSB0', 'baudrate': 115200 }]
bytesize = 8
parity = "None"
stopbits = 1
