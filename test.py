def get_setpoint():
    with open("setpoint.txt", "r") as file:
        read = file.read()
        read = read.split(',')
        x, y = int(read[0]), int(read[1])
    return x, y


while True:
    print(get_setpoint())