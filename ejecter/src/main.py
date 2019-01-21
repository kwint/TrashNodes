import rospy
import RPi.GPIO as GPIO  # import GPIO
import time
from std_msgs.msg import Int16, String
from std_srvs.srv import Trigger
GPIO.setmode(GPIO.BCM)

motor_pin_forw = 1
motor_pin_back = 2
uswitch_pin = 3
rospy.init_node("ejecter")
pub_status = rospy.Publisher("status", String, queue_size=1)

GPIO.setup(motor_pin_forw, GPIO.OUT)
GPIO.setup(motor_pin_back, GPIO.OUT)
GPIO.setup(uswitch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def eject():
    rospy.loginfo("EJECT: Start ejecting")
    startTime = time.time()
    startWeight = rospy.wait_for_message('weight', Int16) # get start weight
    GPIO.output(motor_pin_forw, GPIO.HIGH)

    while time.time() - startTime < 5:
        time.sleep(0.01)

    GPIO.output(motor_pin_forw, GPIO.LOW)

    while True:
        time.sleep(0.01)
        rospy.loginfo("EJECT: Waiting till bag is out of module")
        weight = rospy.wait_for_message('weight', Int16)
        if weight.data < (startWeight.data * 0.5): # Compare current weight with start weight. If weight is 50% of start
            time.sleep(2)
            break                                   # weight the bag has left the module
        if time.time() - startTime > 25:
            pub_status.publish("EJECT: Waiting till bag has been ejected TimeOut")
            rospy.logerr("EJECT: Waiting till bag has been ejected TimeOut")
            return False, "TimeOut"

    GPIO.output(motor_pin_back, GPIO.HIGH)
    while GPIO.input(uswitch_pin) == GPIO.HIGH:
        time.sleep(0.01)

    GPIO.output(motor_pin_back, GPIO.LOW)
    rospy.loginfo("EJECT: Done ejecting")
    pub_status.publish("Done ejecting")
    return True, "Ejecting done"

s = rospy.Service('startEject', Trigger, eject)
rospy.spin()
