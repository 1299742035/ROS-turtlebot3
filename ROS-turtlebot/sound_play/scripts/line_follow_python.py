#!/usr/bin/env python

import sys
import rospy
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Twist
from line_follower_turtlebot.msg import pos

myid = None
mydir = None
move_cmd = None
cmd_vel_pub = None

def is_zero(msg):
    myid = msg

def set_velocity(msg):
    mydir = msg.direction
    if (mydir == 0):
        move_cmd.linear.x = 0.1;
        move_cmd.angular.z = 0.15;
        cmd_vel_pub.publish(move_cmd);
        rospy.sleep(3);
        rospy.loginfo('Turning Left')
    if (mydir == 1):
        move_cmd.linear.x = 0.2;
        move_cmd.angular.z = 0;
        cmd_vel_pub.publish(move_cmd);
        rospy.sleep(3);
        rospy.loginfo('Straight')
    if (mydir == 2):
        move_cmd.linear.x = 0.1;
        move_cmd.angular.z = -0.15;
        cmd_vel_pub.publish(move_cmd);
        rospy.sleep(3);
        rospy.loginfo('Turning Right')
    if (mydir == 3):
        move_cmd.linear.x = 0;
        move_cmd.angular.z = 0.4;
        cmd_vel_pub.publish(move_cmd);
        rospy.sleep(3);
        rospy.loginfo('Searching')



if __name__ == '__main__':
    rospy.init_node('my_line_follow', anonymous=True)

    r = rospy.Rate(30)

    rospy.sleep(1)


    cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
    move_cmd = Twist()

    rospy.wait_for_message('ar_pose_marker', AlvarMarkers)

    rospy.Subscriber('ar_pose_marker', AlvarMarkers, make_sound)

    rospy.Subscriber('direction', pos, set_velocity)

    while not rospy.is_shutdown():
    	rospy.spin()
    	rospy.sleep(1)
