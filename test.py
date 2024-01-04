
def control_conveyor(weight1, weight2):
    try:
        if weight1 is not None and weight2 is not None:
            if weight1 >= 2 and weight2 >= 2:
                # Stop conveyor if either box weighs >= 2
                print("conveyor_stop()")
                #print("greatr than 2")
            elif weight1 < 0 and weight2 < 0:
                # Stop conveyor if both scales read < 0
                 print("conveyor_stop(both)")
            elif weight1 == 0 and weight2 == 0:
                # Stop conveyor if both scales read < 0
                #conveyor_stop()
                 print("conveyor_reverse()")
            elif weight1 <= 0 and weight2 > 2:
                # Start filling the box on the scale that reads 0
                 print("conveyor_forward()")
            elif weight1 > 2 and weight2 <= 0:
                # Start filling the box on the scale that reads 0
                 print("conveyor_reverse()")
            
    except Exception as e:
        print("Error in conveyor control:", e)

w1= float(input(" enter for weight 1 : "))
w2=float(input("enter input for weight 2 : "))
control_conveyor(w1,w2)