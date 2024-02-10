#!/usr/bin/python3

import rospy 
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64


is_done=False
def compute_current_vel(msg):
    global v
    global is_done
    v=msg.twist.twist.linear.x

    print("odom",v)

    is_done=True
    
    return v


def compute_vel(msg):
    global v
    global pub
    global is_done
    global command
    if is_done:
        vsf=msg.data
        print("speed_before",v)
        print("scaling",vsf)
        v=v*vsf
        command.linear.x=v
        pub.publish(command)
        rospy.sleep(0.5) 
        print("speed",v)
    
        is_done=False
        return v







def main():
    global pub
    global v
    global command
    command=Twist()
    rospy.init_node("velocity_controller")
    v=float(input("Enter starting velocity"))
    pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)
    rospy.sleep(1)  #Pour qu'on publie la vitesse a cmd_vel avant les abonnements 
    command.linear.x=v
    pub.publish(command)

    rospy.sleep(0.5)   # Pour que le robot atteigne sa vitesse desirée avant l'abonnement de odom 
    


    
    rospy.Subscriber("/odom",Odometry,compute_current_vel)
    rospy.Subscriber("/scaling",Float64,compute_vel)
    
    rospy.spin()

main()

