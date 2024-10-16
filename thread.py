import serial
import threading
import sm_4rel4in as rel
import time
import re
# Serial ports
ports = ['/dev/ttySC0', '/dev/ttySC1']
# Global flag to signal the loop to continue
terminate_loop = False
# Setup relay board
relay_board = rel.SM4rel4in()
# Global flag to signal threads to stop
terminate_threads = False
forward=1
backward=0
# Global variable to track the time the conveyor stopped
global conveyor_stop_time
conveyor_stop_time = time.time()

def extract_weight(data):
    # Use regular expression to find the weight in the data string
    weights = re.findall(r'-?\s*\d+\.\d+|-?\s*\d+', data)
    
    if weights:
        return float(weights[0].replace(' ', ''))
    else:
        return None

def reset(dir):
    if dir:
        if relay_board.get_relay(1):#if relay 1 is on tuen relay 2 off
            relay_board.set_relay(2, 0)
    else:
        if relay_board.get_relay(2):
            relay_board.set_relay(1, 0)

def conveyor_stop():
    global conveyor_stop_time
    global secondOrder
    # Stop both relays to halt the conveyor
    relay_board.set_relay(1, 0)
    relay_board.set_relay(2, 0)
    relay_board.set_relay(3, 15)
    
    elapsed_time = time.time() - conveyor_stop_time 
    if elapsed_time >= 30 :
        conveyor_stop_time=time.time()
        if not secondOrder:
            for i in range(1):
                # Turn on relay 4 for 2 seconds, then off for 2 seconds, and on again for 2 seconds
                relay_board.set_relay(4, 15)
                time.sleep(2)
                relay_board.set_relay(4, 0)
                time.sleep(2)
                relay_board.set_relay(4, 15)
                time.sleep(2)
                relay_board.set_relay(4, 0)
                time.sleep(2)
                secondOrder =True
                
        elif secondOrder:
            relay_board.set_relay(4, 15)
        
   

def conveyor_forward():
    global conveyor_stop_time
    global secondOrder
    # Turn on relay 1 for forward movement
    relay_board.set_relay(1, 15)
    relay_board.set_relay(2, 0)
    relay_board.set_relay(3, 0)
    relay_board.set_relay(2, 0)
    relay_board.set_relay(4, 0)
    relay_board.set_relay(3, 0)
    relay_board.set_relay(2, 0)
    #relay_board.set_all_relays(8)
    secondOrder =False
    conveyor_stop_time = time.time()

def conveyor_reverse():
    global conveyor_stop_time
    global secondOrder
    # Turn on relay 2 for reverse movement
    relay_board.set_relay(1, 0)
    relay_board.set_relay(2, 15)
    relay_board.set_relay(3, 0)
    relay_board.set_relay(1, 0)
    relay_board.set_relay(4, 0)
    relay_board.set_relay(3, 0)
    relay_board.set_relay(1, 0)##  i needed to call the off multiple times for it to be registered
    #relay_board.set_all_relays(4)
    secondOrder =False
    conveyor_stop_time = time.time()
# I need the conveyor to stop moving instead of switching directions when one scale reads 
# 50 and the other shows anything over 0, however, once the conveyor switches directions it 
# should only stop if/when both scales read 50


def control_conveyor(weight1, weight2):
    try:
        #global conveyor_stop_time
        if weight1 is not None and weight2 is not None:
            if weight1 >= 2 and weight2 >= 2:
                # Stop conveyor if either box weighs >= 2
                conveyor_stop()
                #print("greatr than 2")
            elif weight1 <0 and weight2 >2:
                # Stop filling the box on the scale that reads >2
                conveyor_stop()
            elif weight1 > 0 and weight2 >=2:
                # Stop filling the box on the scale that reads >2
                conveyor_stop()
                
            elif weight1 >=2 and weight2 >0:
                # Stop filling the box on the scale that reads >2
                conveyor_stop()
            elif weight1 >2 and weight2 <0:
                # Stop filling the box on the scale that reads >2
                conveyor_stop()
            elif weight1 < 0.0 and weight2 < 0.0:
                # Stop conveyor if both scales read < 0
                conveyor_stop()
            elif weight1 == 0 and weight2 > 2:
                # Start filling the box on the scale that reads 0
                #reset(forward)
                conveyor_forward()
            elif weight1 == 0 and weight2 < 0:
                # move toward box on the scale that reads 0
                #reset(forward)
                conveyor_forward()
            elif weight1 <0 and weight2 ==0:
                # move towards the box on the scale that reads 0
                #reset(backward)
                conveyor_reverse()
            elif weight1 > 2 and weight2 == 0:
                # Start filling the box on the scale that reads 0
                #reset(backward)
                conveyor_reverse()
            elif weight1 == 0 and weight2 == 0:
                # Stop conveyor if both scales read < 0
                #conveyor_stop()
                #reset(backward)
                global toggle
                toggle = True
                conveyor_reverse()
            
            
    except Exception as e:
        print("Error in conveyor control:", e)

def control_relay1(weight):
    #time.sleep(5)
    #global w1,w2
    try:
        if weight is not None:
            '''
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
                '''
            control_conveyor(w1,w2)
    except Exception as e:
        print("Error in Relay 1 control:", e)

def control_relay2(weight):# all these section is same as using weight 2
    #time.sleep(5)
    #global w1,w2
    try:
        if weight is not None:
            '''
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
                '''
            control_conveyor(w1,w2)
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
                global w1
                w1 = extract_weight(data.decode('utf-8','ignore').strip())
                # Relay control logic
                control_relay1(w1)
                #break
                

def read_serial2(port):
    with serial.Serial(port, baudrate=9600, timeout=1) as ser:
        while True:
            data = ser.readline()
            if data:
                print(f"Data from {port}: {data.decode('utf-8','ignore').strip()}")
                global w2
                w2 = extract_weight(data.decode('utf-8','ignore').strip())
                # Relay control logic
                control_relay2(w2)
                #break

def monitorrelay3():
    if not relay_board.get_relay(1) and not relay_board.get_relay(2):
        relay_board.set_relay(3, 1)
    else :
        relay_board.set_relay(3, 0)
# Creating threads for each scale
thread1 = threading.Thread(target=read_serial, args=('/dev/ttySC0',))
thread2 = threading.Thread(target=read_serial2, args=('/dev/ttySC1',))
thread3=threading.Thread(target=monitorrelay3)

# Starting threads
thread1.start()
thread2.start()
thread3.start()

# Joining threads to the main thread
thread1.join()
thread2.join()
thread3.join()
