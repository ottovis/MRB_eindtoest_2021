import serial
import struct

ser = serial.Serial('COM6', baudrate=9600)

def check_connected():
    global ser
    print("Connected to:", ser.name)
    # ser.write(bytes(b"Hoi"))
    # while ser.in_waiting == 0:
    #     pass
    serialString = ser.readline()
    if b'Hallo\r\n' == serialString:
        return True
    else:
        return False

# # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
# def int_to_bytes(x: int) -> bytes:
#     return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def send_motor_coordinates(x, y, z):
    global ser
    command = x*256*256 + y*256 + z
    command = "% s" % command
    ser.write(bytes(command, encoding='utf-8'))
    ser.write(bytes(b"\r\n"))

if __name__ == '__main__':
    while not check_connected():
        pass
    send_motor_coordinates(100,100,100)
