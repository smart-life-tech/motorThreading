import serial
import threading
import sm_4rel4in as rel
import time
import re
# Setup relay board
relay_board = rel.SM4rel4in()


def extract_weight(data):
    # Use regular expression to find the weight in the data string
    weights = re.findall(r'\d+\.\d+|\d+', data)
    
    if weights:
        return float(weights[0])
    else:
        return None
    
def control_relay1(weight):
    #time.sleep(5)
    try:
        if weight is not None:
            if weight <= 0 and weight2>0:
                # Stop motor if scale 1 shows negative weight
                relay_board.set_relay(1, 0)
            elif weight > 0 and weight < 2:
                # Turn on relay 1 if scale 1 reads 0
                relay_board.set_relay(2, 0)#relay 2 is offkk
                relay_board.set_relay(1, 15)
            elif weight >= 2:
                # Turn off relay 1 if scale 1 reads 2 or more
                relay_board.set_relay(1, 0)
            elif weight1<=0 and weight2<=0:
                relay_board.set_relay(1,15)
    except Exception as e:
        print("Error in Relay 1 control:", e)

def control_relay2(weight):
    #time.sleep(5)
    try:
        if weight is not None:
            if weight <= 0 and weight1 > 0:
                # Stop motor if scale 1 shows negative weight
                relay_board.set_relay(2, 0)
            elif  weight > 0 and weight < 2:
                # Turn on relay 2 if scale 2 reads 0
                relay_board.set_relay(1, 0)#relay 1 is off
                relay_board.set_relay(2, 15)
            elif weight >= 2:
                # Turn off relay 2 if scale 2 reads 2 or more
                relay_board.set_relay( 2, 0)
            elif weight1 >2 and weight2<=0:
                relay_board.set_relay(2, 15)
    except Exception as e:
        print("Error in Relay 2 control:", e)


def control_relay(relay_num, state):
    try:
        if state:
            relay_board.set_relay(relay_num, 15) # Turn relay on
        else:
            relay_board.set_relay(relay_num, 0) # Turn relay off
    except Exception as e:
        print("Error in Relay control:", e)


def read_serial(port):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        while True:
            data = ser.readline()
            if data:
                print(f"Data from {port}: {data.decode('utf-8','ignore').strip()}")
                # Extract weights from data
                global weight1
                weight1 = extract_weight(data.decode('utf-8','ignore').strip())
                # Relay control logic
                control_relay1(weight1)
                

def read_serial2(port):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        while True:
            data = ser.readline()
            if data:
                print(f"Data from {port}: {data.decode('utf-8','ignore').strip()}")
                global weight2
                weight2 = extract_weight(data.decode('utf-8','ignore').strip())
                # Relay control logic
                control_relay2(weight2)

# Creating threads for each scale
thread1 = threading.Thread(target=read_serial, args=('/dev/ttySC0',))
thread2 = threading.Thread(target=read_serial2, args=('/dev/ttySC1',))

# Starting threads
thread1.start()
thread2.start()

# Joining threads to the main thread
thread1.join()
thread2.join()
