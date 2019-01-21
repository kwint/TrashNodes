from hx711 import HX711  # import the class HX711
import RPi.GPIO as GPIO  # import GPIO
import rospy
from std_msgs.msg import Int16

rospy.init_node("loadcells", anonymous=True)
pub = rospy.Publisher("weight", Int16, queue_size=1)
rate = rospy.Rate(0.5)

hx = HX711(dout_pin=21, pd_sck_pin=20, gain_channel_A=64, select_channel='A')
hx2 = HX711(dout_pin=23, pd_sck_pin=22, gain_channel_A=64, select_channel='A')

loadcells = [hx, hx2]
ratios = [[2.8, 2.8],   # 1A, 1B
          [2.8, 2.8]]   # 2A, 2B

offsets = [[-85820, -25050],   # 1A, 1B
          [2.8, 2.8]]   # 2A, 2B

for i, loadcell in enumerate(loadcells):
    result = hx.reset()  # Before we start, reset the hx711 ( not necessary)
    if result:  # you can check if the reset was successful
        print('Ready to use')
    else:
        print('not ready')
    loadcell.set_scale_ratio('A', scale_ratio=ratios[i][0])
    loadcell.set_scale_ratio('B', scale_ratio=ratios[i][1])

    loadcell.set_offset(offsets[i][0], channel='A', gain_A=64)
    loadcell.set_offset(offsets[i][1], channel='B')


ratio = 2.8131269841269821
hx.set_scale_ratio(scale_ratio=ratio)

while not rospy.is_shutdown():
    weight = 0
    for loadcell in loadcells:
        loadcell.select_channel("A")
        weight = weight + loadcell.get_weight_mean(5)
        loadcell.select_channel("B")
        weight = weight + loadcell.get_weight_mean(5)

    pub.publish(weight)
    rate.sleep()
