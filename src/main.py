# ---------------------------------------------------------------------------- #

#                                                                              #

# 	Module:       main.py                                                      #

# 	Author:       vaazhlik                                                     #

# 	Created:      8/12/2026, 8:51:15 AM                                        #

# 	Description:  V5 project event based                                       #

#                                                                              #

# ---------------------------------------------------------------------------- #

# Library imports

# from asyncio import wait

from vex import *

import math

import random



# Brain should be defined by default

brain=Brain()

controller_1 = Controller(PRIMARY)

# Before this section of the code, I made a new one, with polling, and it was useless
# The original code in on main_polling.py

months = 8
days = 16 
file_numb = 1
minutes = 30
hours = 5
years = 26
cur_date=[years, months, days,hours,minutes]
#cur_col = controller_1.screen.column()

log_file_created = False
column_position = controller_1.screen.column()
row_position = controller_1.screen.row()
file_name = "default.csv" #

screen_lock = False #custom mutex api
inertial_1 = Inertial(Ports.PORT17)

def run_date_screen_temporarily():
    """Intializes the screen and 
       Update the current date on controller screen. 
       This """
    global cur_date, screen_lock, column_position, log_file_created 
    #NOTE: if the global column position is not used , a local copy will override this. resulting in screen getting reset to begin

    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1,14)

    column_position = controller_1.screen.column()
    row_position = controller_1.screen.row()

    #for index in range(len(cur_date)):
    #cur_row = controller_1.screen.row()
    #column_position = controller_1.screen.column()

    start_time = brain.timer.time(MSEC)
    last_blink_time = brain.timer.time(MSEC)
    show_cursor = True

    # Setup milestones
    duration_limit = 30000 # Run for 10 seconds (10,000 ms)
    blink_interval = 250   # Blink speed

    ### Bind all the buttons for user inputs
    controller_1.buttonUp.pressed(increment_days)
    controller_1.buttonDown.pressed(decrement_days)
    controller_1.buttonLeft.pressed(move_cursor_left)
    controller_1.buttonRight.pressed(move_cursor_right)
    controller_1.buttonA.pressed(sd_card)

    print ("start timer Column: " + str(column_position) + " Row: " + str(row_position))

    while brain.timer.time(MSEC) - start_time < duration_limit:
        current_time = brain.timer.time(MSEC)

        if not screen_lock:
            screen_lock = True

            if show_cursor:
                controller_1.screen.set_cursor(1,column_position)
                controller_1.screen.print("_")
                controller_1.screen.set_cursor(1,column_position)
                #print(column_position)
            else:
                controller_1.screen.set_cursor(1,1)
                controller_1.screen.print("{:02d}".format(cur_date[0]) +"/" +\
                                    "{:02d}".format(cur_date[1]) +"/" +\
                                    "{:02d}".format(cur_date[2]) +"-" +\
                                    "{:02d}".format(cur_date[3]) +":" +\
                                    "{:02d}".format(cur_date[4]) )
                controller_1.screen.set_cursor(1,column_position)

            show_cursor = not show_cursor
            wait(blink_interval,MSEC)
            #NOTE: if the wait is faster, the blinking effect will not be observed 
            screen_lock = False

        if log_file_created:
            break


    controller_1.screen.clear_screen()


    ### Cleanup button binding
    # controller_1.buttonUp.pressed(None)
    # controller_1.buttonDown.pressed(None)
    # controller_1.buttonLeft.pressed(None)
    # controller_1.buttonRight.pressed(None)
    # controller_1.buttonA.pressed(None)

""""""

def increment_days():
    """
    Increments the day value.
    """
    global months, days, file_numb, setup, column_position, row_position, screen_lock

    #There is no need for this function, when log file is already created
    if log_file_created:
        return
    # I had a problem, the print block automatically moves the cursor to the next coulum automatically
    # To solve this, I made a new variable in each of the incremental sections, as " coulumn "
    # This sets the current coulumn position as a variable
    # That way, I can set the coulumn position after the print() blocks to the position before
    # This variable has to be kept local

    #if not screen_lock:
        #screen_lock = True
    coulumn = column_position
    column_position = controller_1.screen.column()
    column_position = controller_1.screen.column()
    
    row_position = controller_1.screen.row()
    print ("increment_days Column: " + str(column_position) + " Row: " + str(row_position))

    #wait(2,SECONDS)

    index=int(column_position  // 3) # because list index starts with 0, while screen positions starts with 1
    if index <=0:
        index =0

    if index == 0:
        # This is the code for years
        date_part=cur_date[index] % 99 +1

    elif index == 1:
        # This is the code for months
        date_part=cur_date[index] % 12 +1

    elif index == 2:
        # This is the code for days
        date_part=cur_date[index] % 31 +1

    elif index == 3:
        # This is the code for hours
        date_part=cur_date[index] % 23 +1

    elif index == 4:
        # This is the code for minutes
        date_part=cur_date[index] % 59 +1

    else:
        pass 


    print ("increment days date index: " + str(index) + " Row: " + str(row_position))

    #date_part=cur_date[index] % 31 +1
    cur_date[index] = date_part

    #days = days % 31 + 1
    # print ("Days: " + "{:02d}".format(days))
    print ("Column: " + str(column_position) + " Row: " + str(row_position))
    controller_1.screen.set_cursor(1, index*3 )
    #controller_1.screen._column = int(column_position/3)
    # print ("Days: " + "{:02d}".format(date_part))
    controller_1.screen.print("{:02d}".format(date_part))
    controller_1.screen.set_cursor(1,column_position)
    print ("increment_days Column: " + str(column_position) + " Row: " + str(row_position) + " index: "  + str(index) )
    controller_1.screen.set_cursor(1,coulumn)
        #screen_lock = False

def decrement_days():
    """
    Increments the day value.
    """
    global months, days, file_numb, setup, column_position, row_position, screen_lock

    #There is no need for this function, when log file is already created
    if log_file_created:
        return
    
    # I had a problem, the print block automatically moves the cursor to the next coulum automatically
    # To solve this, I made a new variable in each of the incremental sections, as " coulumn "
    # This sets the current coulumn position as a variable
    # That way, I can set the coulumn position after the print() blocks to the position before
    # This variable has to be kept local

    #if not screen_lock:
        #screen_lock = True
    coulumn = column_position
    column_position = controller_1.screen.column()
    column_position = controller_1.screen.column()
    
    row_position = controller_1.screen.row()
    print ("increment_days Column: " + str(column_position) + " Row: " + str(row_position))

    #wait(2,SECONDS)

    index=int(column_position // 3) # because list index starts with 0, while screen positions starts with 1
    # I am experimenting with the index / index, and I feel that the -1 isn't nessesary 
    # Here is the original line of code:
    # index=int(column_position // 3)-1 # because list index starts with 0, while screen positions starts with 1

    if index <=0:
        index =0

    print ("increment days date index: " + str(index) + " Row: " + str(row_position))

    date_part=cur_date[index] % 31 -1
    if date_part <= 0:
        date_part = 31
    cur_date[index] = date_part

    #days = days % 31 + 1
    # print ("Days: " + "{:02d}".format(days))
    print ("Column: " + str(column_position) + " Row: " + str(row_position))
    controller_1.screen.set_cursor(1, index*3 )
    #controller_1.screen._column = int(column_position/3)
    # print ("Days: " + "{:02d}".format(date_part))
    controller_1.screen.print("{:02d}".format(date_part))
    controller_1.screen.set_cursor(1,column_position)
    print ("increment_days Column: " + str(column_position) + " Row: " + str(row_position) + " Last coulumn position: "  + str(coulumn) )
    controller_1.screen.set_cursor(1,coulumn)
        #screen_lock = False


def move_cursor_left():
    """
    Moves the cursor one position to the left.
    """
    global column_position, row_position, screen_lock
    #NOTE: Acquire the right to update the screen 
    while not screen_lock:
        screen_lock = True

    print("move cur left - Column: " + str(column_position) + " Row: " + str(row_position))

    column_position = controller_1.screen.column()
    #row_position = controller_1.screen.row()

    column_position = (column_position - 1) #%15
    if column_position <=0:
        column_position = 1
    print(" move cur left - Column: " + str(column_position) + " Row: " + str(row_position))

    controller_1.screen.set_cursor(1, column_position)
    controller_1.screen.print("_")
    controller_1.screen.set_cursor(1, column_position)

    #NOTE: Free the screen lock to facilitate date update
    screen_lock = False


def move_cursor_right():
    """
    Moves the cursor one position to the right.
    """
    global months, days, file_numb, setup, column_position, row_position, screen_lock

    #NOTE: Acquire the right to update the screen 
    while not screen_lock:
        screen_lock = True

    #column_position = controller_1.screen.column()
    print("move cur right - Column: " + str(column_position) + " Row: " + str(row_position))

    row_position = controller_1.screen.row()
    print("move cur right - Column: " + str(column_position) + " Row: " + str(row_position))

    #NOTE: Is there is a spelling mistake in the variable name, python will silently create a new variable
    #this is dangerous, leading unexpected behavior eg. column and coulumn
    column_position = (column_position + 1) % 15
    controller_1.screen.set_cursor(1, column_position)
    column_position = controller_1.screen.column()

    print("new Column: " + str(column_position) + " Row: " + str(row_position))
    controller_1.screen.print("_")
    controller_1.screen.set_cursor(1, column_position)

    print("new Column: " + str(column_position) + " Row: " + str(row_position))

    #give up the right to update the screen, so that screen refresh timer can run
    #screen_lock = False



def initialize() :
    """
    Initialize the system by creating an initial storage log file(recent_file.txt) to track time history

    """
    global cur_date


    if brain.sdcard.exists("recent_file.txt"):
        #brain.sdcard.exists

        try:
            with open("recent_file.txt", "r") as file:
            #file.read("timestamp,arm_position_deg,arm_velocity_rpm,arm_torque_nm,arm_power_w")
                content = file.read(14)
                print("----->"+str(content))


            #FIXED: when recent_file exist. read the content and increment the minute

            content_as_list = content.split('-')
            print("content_as_list"+str(content_as_list))
            try:
                for idx in range(4):
                    cur_date[idx]=int(content_as_list[idx])
                    print("cur_date["+str(idx)+"]="+str(cur_date[idx]))
                print("came here")  

            except Exception as e:
                    print("received exception at 334 "+str(e.with_traceback))



            date_part = content.split("-")[-1]
            print("date :"+str(content)+ " mm:"+date_part )
            cur_date[4] = (int(date_part) +1) % 59
            print("incremented date :"+str(cur_date)+ " mm:"+date_part )


        except Exception as e:
            print("Error reading file: " + str(e.with_traceback))

    else:
        print("no such file in sd Card")
        brain.screen.print("Dude! Did you insert the SD card ? ")
        brain.sdcard.savefile("recent_file.txt")
        #brain.sdcard.("recent_file.txt", )
        #brain.sdcard.file.read 

    # #save the current date into the recent file.txt    !!!!!! is it even required ?
    # with open("recent_file.txt","w") as file:
    #     recent_file_name = "{:02d}".format(cur_date[0]) +"-" +\
    #                             "{:02d}".format(cur_date[1]) +"-" +\
    #                             "{:02d}".format(cur_date[2]) +"-" +\
    #                             "{:02d}".format(cur_date[3]) +"-" +\
    #                             "{:02d}".format(cur_date[4])
    #     file.write(recent_file_name)


         
def sd_card ():
    global cur_date #NOTE: without this line date will not be updated in the recent_files
    global file_name #NOTE: without this line, all new writings happen in default.csv in global
    global log_file_created
    if controller_1.buttonA.pressed:
        if brain.sdcard.is_inserted():
            file_name = "{:02d}".format(cur_date[0]) +"-" +\
                                    "{:02d}".format(cur_date[1]) +"-" +\
                                    "{:02d}".format(cur_date[2]) +"-" +\
                                    "{:02d}".format(cur_date[3]) +"-" +\
                                    "{:02d}".format(cur_date[4]) + ".csv"
            try:
                with open(file_name, "w") as file:
                    #write the CSV file header
                    file.write("timestamp,arm_position_deg,arm_velocity_rpm,arm_torque_nm,arm_power_w,arm_current\n")
                    print("File saved as:" +file_name)
                    print(file_name)  

                with open("recent_file.txt","w") as recent_file:
                        last_file_date = "{:02d}".format(cur_date[0]) +"-" +\
                                    "{:02d}".format(cur_date[1]) +"-" +\
                                    "{:02d}".format(cur_date[2]) +"-" +\
                                    "{:02d}".format(cur_date[3]) +"-" +\
                                    "{:02d}".format(cur_date[4])
                        recent_file.write(last_file_date)

            except Exception as e:
                print("Error saving file: " + str(e))
                                         
        else:
            brain.screen.print("Error: No SD card")
    else:
        controller_1.screen.print("Please connect SD card")

    log_file_created = True


#######################################

def lift_weight():
    global file_name
    arm_motor_l = Motor(Ports.PORT5, GearSetting.RATIO_36_1, False)
    arm_motor_l.set_stopping(BrakeType.HOLD)
    arm_motor_l.set_velocity(50, PERCENT)

    arm_motor_r=Motor(Ports.PORT15, GearSetting.RATIO_36_1, False)
    arm_motor_r.set_stopping(BrakeType.HOLD)
    arm_motor_r.set_velocity(50, PERCENT)

    while True:
        if controller_1.buttonUp.pressing():
            arm_motor_l.spin(DirectionType.FORWARD)
            arm_motor_r.spin(DirectionType.REVERSE)

        elif controller_1.buttonDown.pressing():
            arm_motor_l.spin(DirectionType.REVERSE)
            arm_motor_r.spin(DirectionType.FORWARD)
                    
        else:
            arm_motor_l.stop()
            arm_motor_r.stop()

    
        #capture essential motor attributes
        t_stamp = brain.timer.value()
        pos = arm_motor_l.position(DEGREES)
        vel = arm_motor_l.velocity(RPM)
        torque = arm_motor_l.torque(TorqueUnits.NM)
        power = arm_motor_l.power(PowerUnits.WATT) 
        current = arm_motor_l.current(CurrentUnits.AMP)

        pos_r = arm_motor_r.position(DEGREES)
        vel_r = arm_motor_r.velocity(RPM)
        torque_r = arm_motor_r.torque(TorqueUnits.NM)
        power_r = arm_motor_r.power(PowerUnits.WATT)
        current_r = arm_motor_r.current(CurrentUnits.AMP)

        # Format log entry
        log_entry = "{:.3f}".format(t_stamp) +"," +\
                                "{:.2f}".format(pos) +"," +\
                                "{:.2f}".format(vel) +"," +\
                                "{:.3f}".format(torque) +"," +\
                                "{:.3f}".format(power)+"," +\
                                "{:.3f}".format(current)+","+\
                                "{:.2f}".format(pos_r) +"," +\
                                "{:.2f}".format(vel_r) +"," +\
                                "{:.3f}".format(torque_r) +"," +\
                                "{:.3f}".format(power_r)+"," +\
                                "{:.3f}".format(current_r)+"\n"


        #print(log_entry)
        
        # Append attributes to log file on SD card
        try:
            with open(file_name, "a") as f:
                f.write(log_entry)
        except Exception as e:
                brain.screen.print("File write failed")
                print("file write failed exception"+str(e.with_traceback))

# Call at startup
#load_time_from_largest_file()















# -------------------------------------------------------------------------------------------------------------------#


#Objectives for today, 8/14/26
"""
# Step #1, program the up button and the down button to move to the respective position that the cusror is blinking at. 
# Currently, the up arrow and down arrow only work for the years. 
# Even though the cursor moves to the right to the months feild.
"""

# Step #1 is finished


# Step #2
# I need to make the code dounload into the file as the name.
# This bit of code is for the file renaming process. It is going to take the final date

# For one thing, I need to figure out why the indents 
# are weird on the code below

"""
.format(cur_date[0]) +"/" +\
                                    "{:02d}".format(cur_date[1]) +"/" +\
                                    "{:02d}".format(cur_date[2]) +"-" +\
                                    "{:02d}".format(cur_date[3]) +":" +\
                                    "{:02d}".format(cur_date[4]) )
""" 
def write_2_sd_card():
    if brain.sdcard.is_inserted():
    # Create data to save (must be bytearray)
            data = bytearray("{:02d}".format(cur_date[0]) +"/" +\
                            "{:02d}".format(cur_date[1]) +"/" +\
                                "{:02d}".format(cur_date[2]) +"-" +\
                                "{:02d}".format(cur_date[3]) +":" +\
                                "{:02d}".format(cur_date[4]), 'utf-8' )
"""
def sd_card ():
    if controller_1.buttonA.pressed:
        if brain.sdcard.is_inserted():
            brain.sdcard.savefile(filename, data)
            brain.screen.print(f"Saved: {filename}")
        else:
            brain.screen.print("Error: No SD card")
    else:
        controller_1.screen.print("Please connect SD card")
"""



    # Save file with timestamp as name

# -------------------------------------------------------------------------------------------------- #

# Objectives for today: (8/15/26)



    # I had a problem, the print block automatically moves the cursor to the next coulum automatically
    # To solve this, I made a new variable in each of the incremental sections, as " coulumn "
    # This sets the current coulumn position as a variable
    # That way, I can set the coulumn position after the print() blocks to the position before
    # This variable has to be kept local



## ------------------------------------------------------------------------------------------------------ ##


def Move_Forward():
    global file_name
    front_right = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
    back_left = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)

    front_right.set_stopping(BrakeType.HOLD)
    back_left.set_stopping(BrakeType.HOLD)
    front_right.set_velocity(50, PERCENT)
    back_left.set_velocity(50, PERCENT)

    while True:
        if controller_1.buttonUp.pressing():
            front_right.spin(DirectionType.FORWARD)
            back_left.spin(DirectionType.FORWARD)
        elif controller_1.buttonDown.pressing():
            front_right.spin(DirectionType.REVERSE)
            back_left.spin(DirectionType.REVERSE)
        else:
            front_right.stop()
            back_left.stop()
            break

def callibrate_sensors():
    global inertial_1
    inertial_1 = Inertial(Ports.PORT17)

    if inertial_1.installed():
        print("Inertial sensor is installed.")
        # Start calibration.
        inertial_1.calibrate()
    else:
        print("Inertial sensor is not installed.")

def wait_for_calibration():
        global inertial_1
        while inertial_1.is_calibrating():
            print("Calibrating...")
            wait(100, MSEC)
        print("Calibration complete.")
        brain.screen.print("Calibration complete.")

def drive_straight(direction=FORWARD, dist=1, units=TURNS):
    rot=inertial_1.rotation()
    FRONT_RIGHT = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
    FRONT_LEFT = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
    BACK_LEFT = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
    BACK_RIGHT = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
    FRONT_RIGHT.spin_for(direction, dist, TURNS, wait=False)
    BACK_RIGHT.spin_for(direction, dist, TURNS, wait=False)

    if direction == FORWARD:
        direction = REVERSE
    else:
        direction = FORWARD

    FRONT_LEFT.spin_for(direction, dist, TURNS, wait=False)
    BACK_LEFT.spin_for(direction, dist, TURNS, wait=True)    
    wait(1000, MSEC)
    rot=inertial_1.rotation()

    brain.screen.print("Rotation: {:.2f} degrees".format(rot))

    return
################################################################
# ------------------------------------------------------------
# FRONT LEFT MOTOR
# Port 1
# ------------------------------------------------------------

front_left = Motor(
    Ports.PORT1,
    GearSetting.RATIO_18_1,
    False
)



# ------------------------------------------------------------
# FRONT RIGHT MOTOR
# Port 2
#
# True means the motor direction is reversed in software.
# ------------------------------------------------------------

front_right = Motor(
    Ports.PORT10,
    GearSetting.RATIO_18_1,
    True
)



# ------------------------------------------------------------
# BACK RIGHT MOTOR
# Port 3
# ------------------------------------------------------------

back_right = Motor(
    Ports.PORT20,
    GearSetting.RATIO_18_1,
    True
)



# ------------------------------------------------------------
# BACK LEFT MOTOR
# Port 4
# ------------------------------------------------------------

back_left = Motor(
    Ports.PORT11,
    GearSetting.RATIO_18_1,
    False
)



# ============================================================
# 3. CREATE LEFT AND RIGHT DRIVE MOTOR GROUPS
# ============================================================

# LEFT SIDE:
#
# Port 1 = Front Left
# Port 4 = Back Left

left_drive = MotorGroup(
    front_left,
    back_left
)


# RIGHT SIDE:
#
# Port 2 = Front Right
# Port 3 = Back Right

right_drive = MotorGroup(
    front_right,
    back_right
)



# ============================================================
# 4. DRIVE SETTINGS
# ============================================================

# When the joystick goes back to center,
# BRAKE helps stop the robot instead of letting it coast.

front_left.set_stopping(BRAKE)
front_right.set_stopping(BRAKE)
back_right.set_stopping(BRAKE)
back_left.set_stopping(BRAKE)


# Ignore tiny joystick movements.
DEADZONE = 5



# ============================================================
# 5. LIMIT MOTOR SPEED
# ============================================================

def limit_speed(speed):

    # Never command more than +100%.
    if speed > 100:
        return 100

    # Never command less than -100%.
    if speed < -100:
        return -100

    return speed



# ============================================================
# 6. STOP THE COMPLETE DRIVETRAIN
# ============================================================

def stop_drive():

    left_drive.stop(BRAKE)

    right_drive.stop(BRAKE)



# ============================================================
# 7. DRIVE ROBOT USING CONTROLLER
# ============================================================

def drive_robot():

    # --------------------------------------------------------
    # READ FORWARD / BACKWARD
    # --------------------------------------------------------

    # Axis 3 is the LEFT joystick.
    #
    # +100 = full forward
    #    0 = centered
    # -100 = full backward

    forward = controller_1.axis3.position()



    # --------------------------------------------------------
    # READ LEFT / RIGHT TURN
    # --------------------------------------------------------

    # Axis 1 is the RIGHT joystick.
    #
    # Positive = right
    # Negative = left

    turn = controller_1.axis1.position()



    # ========================================================
    # ARCADE DRIVE CALCULATION
    # ========================================================

    # LEFT SIDE:
    #
    # Forward + Turn

    left_speed = forward + turn


    # RIGHT SIDE:
    #
    # Forward - Turn

    right_speed = forward - turn



    # ========================================================
    # KEEP MOTOR COMMANDS BETWEEN -100% AND +100%
    # ========================================================

    left_speed = limit_speed(left_speed)

    right_speed = limit_speed(right_speed)



    # ========================================================
    # APPLY DEADZONE
    # ========================================================

    # Prevent robot from slowly moving because of
    # tiny joystick readings.

    if abs(left_speed) < DEADZONE:
        left_speed = 0


    if abs(right_speed) < DEADZONE:
        right_speed = 0



    # ========================================================
    # SEND SPEED TO LEFT SIDE
    # ========================================================

    # Controls:
    #
    # Port 1 = Front Left
    # Port 4 = Back Left

    left_drive.spin(
        FORWARD,
        left_speed,
        PERCENT
    )



    # ========================================================
    # SEND SPEED TO RIGHT SIDE
    # ========================================================

    # Controls:
    #
    # Port 2 = Front Right
    # Port 3 = Back Right

    right_drive.spin(
        FORWARD,
        right_speed,
        PERCENT
    )




def measure_motor_attributes(duration_ms=500000, sample_period_ms=100):
    """
    Run all four drive motors briefly and log their raw operating data to an
    SD card CSV file. This helps understand each motor's behavior and the load
    being applied during motion.
    """
    global file_name

    if not brain.sdcard.is_inserted():
        brain.screen.print("Insert SD card")
        return

    # Use the same four drive motors in the robot chassis.
    motors = {
        "FR": Motor(Ports.PORT11, GearSetting.RATIO_18_1, False),
        "FL": Motor(Ports.PORT20, GearSetting.RATIO_18_1, False),
        "BL": Motor(Ports.PORT10, GearSetting.RATIO_18_1, False),
        "BR": Motor(Ports.PORT1, GearSetting.RATIO_18_1, False),
    }

    for motor in motors.values():
        motor.set_stopping(BrakeType.HOLD)
        motor.set_velocity(35, PERCENT)

    # Left-side motors are mounted opposite the right-side motors, so their
    # direction must be inverted to represent the same logical forward drive.
    left_motors = [motors["FL"], motors["BL"]]
    right_motors = [motors["FR"], motors["BR"]]

    for motor in left_motors:
        motor.spin(DirectionType.REVERSE)
    for motor in right_motors:
        motor.spin(DirectionType.FORWARD)

    # timestamp = "motor_attributes_" + "{:02d}".format(cur_date[0]) + "-" + \
    #     "{:02d}".format(cur_date[1]) + "-" + \
    #     "{:02d}".format(cur_date[2]) + "-" + \
    #     "{:02d}".format(cur_date[3]) + "-" + \
    #     "{:02d}".format(cur_date[4]) + ".csv"

    with open(file_name, "w") as log_file:
        log_file.write(
            "time_ms,"
            "FR_position_deg,FR_velocity_rpm,FR_torque_nm,FR_power_w,FR_current_a,"
            "FL_position_deg,FL_velocity_rpm,FL_torque_nm,FL_power_w,FL_current_a,"
            "BL_position_deg,BL_velocity_rpm,BL_torque_nm,BL_power_w,BL_current_a,"
            "BR_position_deg,BR_velocity_rpm,BR_torque_nm,BR_power_w,BR_current_a\n"
        )

    start_time = brain.timer.time(MSEC)

    while brain.timer.time(MSEC) - start_time < duration_ms:
        elapsed = brain.timer.time(MSEC) - start_time
        data_row = [str(elapsed)]

        for name, motor in motors.items():
            pos = motor.position(DEGREES)
            vel = motor.velocity(RPM)
            torque = motor.torque(TorqueUnits.NM)
            power = motor.power(PowerUnits.WATT)
            current = motor.current(CurrentUnits.AMP)
            data_row.extend([
                str(pos),
                str(vel),
                str(torque),
                str(power),
                str(current),
            ])

        with open(file_name, "a") as log_file:
            log_file.write(",".join(data_row) + "\n")

        wait(sample_period_ms, MSEC)

    for motor in motors.values():
        motor.stop()

    brain.screen.print("Saved: " + file_name)
    return file_name

    

initialize()
callibrate_sensors()
run_date_screen_temporarily()
wait_for_calibration()

drive_straight(FORWARD, 10, TURNS)
while true:
    drive_robot()
    lift_weight()
    wait(20, MSEC)  # Small delay to prevent CPU overload
    
# date_screen_temporarily() hold all the other defs, so when it timed runs, all defs run together
#drive_straight(FORWARD, 1, TURNS)
#measure_motor_attributes()
