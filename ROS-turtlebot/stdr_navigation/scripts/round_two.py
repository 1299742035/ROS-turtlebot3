#!/usr/bin/env python
# -*- coding: UTF-8 -*-
     
import rospy
import random
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
     
class PatrolNav():
     
    def __init__(self):
        rospy.init_node('patrol_nav_node', anonymous=False)
        rospy.on_shutdown(self.shutdown)
     
        # From launch file get parameters
        self.rest_time     = rospy.get_param("~rest_time", 2)
        self.keep_patrol   = rospy.get_param("~keep_patrol",   False)
        self.random_patrol = rospy.get_param("~random_patrol", False)
        self.patrol_type   = rospy.get_param("~patrol_type", 0)
        self.patrol_loop   = rospy.get_param("~patrol_loop", 5)
        self.patrol_time   = rospy.get_param("~patrol_time", 5)
     
        #set all navigation target pose
        self.locations = dict()
        self.locations['PS1']   = Pose(Point(1.3167, -0.1066, 0.000), Quaternion(0.000, 0.000, 0.987815, 0.155627))
        self.locations['AR1']   = Pose(Point(-0.3476,  0.2827, 0.000), Quaternion(0.000, 0.000, 0.991664,  0.128843))
        self.locations['PS2'] = Pose(Point(2.6036, 3.5758, 0.000), Quaternion(0.000, 0.000,-0.760863, 0.648911))
        self.locations['AR2']   = Pose(Point( 2.3106,  2.7577, 0.000), Quaternion(0.000, 0.000,  0.987931,  0.154893))
        self.locations['PS3']   = Pose(Point(1.3167, -0.1066, 0.000), Quaternion(0.000, 0.000, 0.987815, 0.155627))
        self.locations['AR3']   = Pose(Point(-0.3476,  0.2827, 0.000), Quaternion(0.000, 0.000, 0.991664,  0.128843))
        self.locations['PS4'] = Pose(Point(2.6036, 3.5758, 0.000), Quaternion(0.000, 0.000,-0.760863, 0.648911))
        self.locations['AR4']   = Pose(Point( 2.3106,  2.7577, 0.000), Quaternion(0.000, 0.000,  0.987931,  0.154893))

        # Goal state return values
        goal_states = ['PENDING', 'ACTIVE', 'PREEMPTED', 'SUCCEEDED', 'ABORTED',
                       'REJECTED', 'PREEMPTING', 'RECALLING', 'RECALLED', 'LOST']
     
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(30))
        rospy.loginfo("Connected to move base server")
     
        # Variables to keep track of success rate, running time etc.
        loop_cnt = 0
        n_goals  = 0
        n_successes  = 0
        target_num   = 0
        running_time = 0
        location   = ""
        start_time = rospy.Time.now()
        locations_cnt = len(self.locations)
        #sequeue = ['PS1', 'AR1', 'PS2', 'AR2', 'PS3', 'AR3', 'PS4', 'AR4']
        sequeue = ['PS1', 'PS2', 'PS3', 'PS4', 'PS1', 'PS2', 'PS3', 'PS4']
     
        rospy.loginfo("Starting position navigation ")
        # Begin the main loop and run through a sequence of locations
        while not rospy.is_shutdown():
            #judge if set keep_patrol is true
            if self.keep_patrol == False:
                if self.patrol_type == 0: #use patrol_loop
                    if target_num == locations_cnt :
                        if loop_cnt < self.patrol_loop-1:
                            target_num = 0
                            loop_cnt  += 1
                            rospy.logwarn("Left patrol loop cnt: %d", self.patrol_loop-loop_cnt)
                        else:
                            rospy.logwarn("Now patrol loop over, exit...")
                            rospy.signal_shutdown('Quit')
                            break
            else:
                if self.random_patrol == False:
                    if target_num == locations_cnt:
                        target_num = 0
                else:
                    target_num = random.randint(0, locations_cnt-1)
     
            # Get the next location in the current sequence
            location = sequeue[target_num]
            rospy.loginfo("Going to: " + str(location))
            self.send_goal(location)
     
            # Increment the counters
            target_num += 1
            n_goals    += 1
     
            # Allow 5 minutes to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(300))
            # Check for success or failure
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.logerr("ERROR:Timed out achieving goal")
            else:
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    n_successes += 1
                    rospy.loginfo("Goal succeeded!")
                else:
                    rospy.logerr("Goal failed with error code:"+str(goal_states[state]))
     
            # How long have we been running?
            running_time = rospy.Time.now() - start_time
            running_time = running_time.secs/60.0
     
            # Print a summary success/failure and time elapsed
            rospy.loginfo("Success so far: " + str(n_successes) + "/" +
                          str(n_goals) + " = " +
                          str(100 * n_successes/n_goals) + "%")
            rospy.loginfo("Running time: " + str(self.trunc(running_time, 1)) + " min")
            rospy.sleep(self.rest_time)
     
            if self.keep_patrol == False and self.patrol_type == 1: #use patrol_time
                if running_time >= self.patrol_time:
                    rospy.logwarn("Now reach patrol_time, back to original position...")
                    self.send_goal('six')
                    rospy.signal_shutdown('Quit')
     
    def send_goal(self, locate):
        # Set up the next goal location
        self.goal = MoveBaseGoal()
        self.goal.target_pose.pose = self.locations[locate]
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.header.stamp = rospy.Time.now()
        self.move_base.send_goal(self.goal) #send goal to move_base
     
    def trunc(self, f, n):
        # Truncates/pads a float f to n decimal places without rounding
        slen = len('%.*f' % (n, f))
        return float(str(f)[:slen])
     
    def shutdown(self):
        rospy.logwarn("Stopping the patrol...")
     
if __name__ == '__main__':
    try:
        PatrolNav()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.logwarn("patrol navigation exception finished.")
