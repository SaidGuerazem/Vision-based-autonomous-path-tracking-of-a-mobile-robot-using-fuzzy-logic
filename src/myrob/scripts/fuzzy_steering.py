#!/usr/bin/python3
import numpy as np 
import rospy
import skfuzzy as fuzzy
from myrob.msg import error
from myrob.msg import bends
from std_msgs.msg import Float64
from skfuzzy import control as ctrl

#Still not sure how to define the max value , I think it needs to be done by defining the angular velocity
#and then depending on the current velocity u get the max steering angle 
#that part still needs work

#made them global  variables cause I need them in both functions 
phi=None
phi_max=1.57
vsf=None

#Just made a flag to make the second subscriber start only after getting the steering angle from the first subscriber "it's an argument for the second callback"
is_done=False

# universe of discourse
universe=np.arange(-1,1.01,0.01)
output_universe=np.arange(-10,10,0.01)

# inputs
e1=ctrl.Antecedent(universe,'e1')
e2=ctrl.Antecedent(universe,'e2')



# membership functions

#je l'ai créé de cette manière pour avoir une forme d'une function s et z , mais sans interpolation , juste en modifiant la forme trapezoidale.
# 3 et -3 sont aleatoire, on vas jamais depasser le -1 et 1 de toute façon

positive=fuzzy._membership.trapmf(universe,[-1,1,3,3])
negative=fuzzy._membership.trapmf(universe,[-3,-3,-1,1])


def compute_firing_strength1(e1,e2,A1i,A2i):
    # calculate the degree of membership 
    mu_A1i=fuzzy.interp_membership(universe,A1i,e1)
    mu_A2i=fuzzy.interp_membership(universe,A2i,e2)

    return mu_A1i*mu_A2i


#Compute using weighted average method
def compute_output1(msg, gamma1=1, gamma2=1, gamma3=1, gamma4=1, a1=9, a2=-0.02):
    global phi
    global is_done
    
    e11=msg.e1
    e22=msg.e2
    A1 = [positive, positive, negative, negative]
    A2 = [positive, negative, positive, negative]

    gamma1_val = compute_firing_strength1(e11, e22, A1[0], A2[0]) * gamma1
    gamma2_val = compute_firing_strength1(e11, e22, A1[1], A2[1]) * gamma2
    gamma3_val = compute_firing_strength1(e11, e22, A1[2], A2[2]) * gamma3
    gamma4_val = compute_firing_strength1(e11, e22, A1[3], A2[3]) * gamma4

    numerator = (gamma1_val + gamma4_val) * (a1 * e11 + a2 * e22)
    denominator = gamma1_val + gamma2_val + gamma3_val + gamma4_val
   
    phi=numerator / denominator

    is_done=True
    
    return phi

#universe

steering_univ=np.arange(-1,1.01,0.01)
bend_univ=np.arange(0,1.01,0.01)
vsf_univ=np.arange(0.2,1.01,0.01)

#inputs

steering=ctrl.Antecedent(steering_univ,'steering')
bend=ctrl.Antecedent(bend_univ,'steering')

#outputs


#membership functions
#steering 


Gentle=fuzzy._membership.trapmf(steering_univ,[-3,-3,-1,0])
Appropriate=fuzzy._membership.trimf(steering_univ,[-1,0,1])
Aggressive=fuzzy._membership.trapmf(steering_univ,[0,1,3,3])


#bend 

Wide=fuzzy._membership.trapmf(bend_univ,[-3,-3,0,0.5])
Medium=fuzzy._membership.trimf(bend_univ,[0,0.5,1])
Narrow=fuzzy._membership.trapmf(bend_univ,[0.5,1,3,3])


def compute_firing_strength2(steering,bend,A1i,A2i):
    # calculate the degree of membership 
    mu_A1i=fuzzy.interp_membership(steering_univ,A1i,steering)
    mu_A2i=fuzzy.interp_membership(bend_univ,A2i,bend)

    return mu_A1i*mu_A2i


def compute_output2(msg,low=0.2, medium=0.5, high=1):
    global phi 
    global vsf
    global phi_max
    global is_done 

    if is_done:
        steering=phi-phi_max
        bend=msg.c_norm
        A1 = [Gentle, Appropriate,Aggressive]
        A2 = [Wide, Medium, Narrow]
        fs=[]
        i=0 
        j=0
        for i in range(3) :
            for j in range(3):
                fs_ij= compute_firing_strength2(steering, bend, A1[i], A2[j])
                fs.append(fs_ij)
    

        numerator=(fs[0]*high)+(fs[1]*high)+(fs[2]*medium)+(fs[3]*high)+(fs[4]*medium)+(fs[5]*low)+(fs[6]*medium)+(fs[7]*low)+(fs[8]*low)
        denominator=sum(fs)
        vsf=numerator/denominator

        return vsf

def main():
    global is_done
    rospy.init_node("controllers")
    rospy.Subscriber("/error",error,compute_output1)
    rospy.Subscriber("/bend",bends,compute_output2)
    pub1=rospy.Publisher("/steering",Float64,queue_size=10)
    pub2=rospy.Publisher("/scaling",Float64,queue_size=10)
    is_done=False


    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        
        pub1.publish(phi)
        pub2.publish(vsf)
        rate.sleep()
    

main()

