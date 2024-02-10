#!/usr/bin/python3

import rospy 
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64
from myrob.msg import error

v=None
is_done=False
def compute_current_vel(msg):
    global v
    global is_done
    v=msg.e1
    is_done=True
    print(3)
    
    return v


def compute_vel(msg):
    global v
    global is_done
    global pub
    if is_done:
        vsf=msg.data
        v=v*vsf
        if v is not None:
            pub.publish(v)
            return v







def main():
    global v
    global is_done
    global pub
    rospy.init_node("velocity_controller")
    v=float(input("What is love ?"))

    pub=rospy.Publisher("/Tester",Float64,queue_size=10)

    rospy.sleep(4)

    pub.publish(v)

    
    rospy.Subscriber("/error",error,compute_current_vel)
    rospy.Subscriber("/scaling",Float64,compute_vel)
    
        
    rospy.spin()

    
    

main()


