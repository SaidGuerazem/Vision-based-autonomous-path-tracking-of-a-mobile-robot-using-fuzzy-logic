#!/usr/bin/python3

import rospy 
from myrob.msg import bend
from myrob.msg import error 






def main():
    rospy.init_node('sender')
    pub1=rospy.Publisher("/error",error,queue_size=10)
    pub2=rospy.Publisher("/bend",bend,queue_size=10)

    error_msg=error()
    bend_msg=bend()
    rate=rospy.Rate(10)

    while not rospy.is_shutdown():
        

        error.e1=0.2
        error.e2=0.5
        bend.c_norm=0.2
        

        

        pub1.publish(error_msg)
        pub2.publish(bend_msg)

        rate.sleep()



main()