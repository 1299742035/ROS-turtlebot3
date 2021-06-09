#!/usr/bin/env python

#***********************************************************
#* Software License Agreement (BSD License)
#*
#*  Copyright (c) 2009, Willow Garage, Inc.
#*  All rights reserved.
#*
#*  Redistribution and use in source and binary forms, with or without
#*  modification, are permitted provided that the following conditions
#*  are met:
#*
#*   * Redistributions of source code must retain the above copyright
#*     notice, this list of conditions and the following disclaimer.
#*   * Redistributions in binary form must reproduce the above
#*     copyright notice, this list of conditions and the following
#*     disclaimer in the documentation and/or other materials provided
#*     with the distribution.
#*   * Neither the name of the Willow Garage nor the names of its
#*     contributors may be used to endorse or promote products derived
#*     from this software without specific prior written permission.
#*
#*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#*  POSSIBILITY OF SUCH DAMAGE.
#***********************************************************

import sys
import rospy
import os
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Twist
from line_follower_turtlebot.msg import pos

myid = None
move_cmd = None
soundhandle = None


def make_sound(msg):
	try:
		marker = msg.markers[0]
		rospy.loginfo('find the marker')
	except:
		rospy.loginfo('i cannot find the marker')
		return

	myid = marker.id
	rospy.loginfo('the number is : '+str(myid))
	soundhandle.say(str(myid), 'voice_kal_diphone', 5)
	r.sleep()


if __name__ == '__main__':
	rospy.init_node('play')
	r = rospy.Rate(10)

	soundhandle = SoundClient()
	r.sleep()

	move_cmd = Twist()

	rospy.wait_for_message('ar_pose_marker', AlvarMarkers)

	rospy.Subscriber('ar_pose_marker', AlvarMarkers, make_sound)

	while not rospy.is_shutdown():
		rospy.spin()
		r.sleep()
