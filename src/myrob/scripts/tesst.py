#!/usr/bin/python3

import rospy 
from std_msgs.msg import Float64






def main():
    rospy.init_node("steerer")
    pub=rospy.Publisher("/caster_rear_joint_position_controller/command",Float64,queue_size=10)
    rate=rospy.Rate(5)
    while not rospy.is_shutdown():
        phi=1.46
        pub.publish(phi)
        rospy.sleep(2)
        # phi=1.046
        # pub.publish(phi)
        # rospy.sleep(2)
        # phi=1.57
        # pub.publish(phi)
        # rospy.sleep(2)
        # phi=-0.628
        # pub.publish(phi)
        # rospy.sleep(2)
        phi=-1.46
        pub.publish(phi)
        rospy.sleep(2)
        # phi=-1.57
        # pub.publish(phi)
        # rospy.sleep(2)
        rate.sleep()


main()
