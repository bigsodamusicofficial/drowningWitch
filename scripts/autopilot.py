# fake radar for testing
# big soda

import tf
import math
import rospy
import numpy
import random
from itertools import chain
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Point, Quaternion
from visualization_msgs.msg import Marker

import ast
from ast import literal_eval as make_tuple

import fake_boats

map_scalar = 4.0

class autopilot:
    def __init__(self):
        self.objects = []

        self.me = fake_boats.boat()
        self.me.coords = (0, 100 * map_scalar)
        self.me.speed = 2.0
        self.me.angle = math.pi

        self.waypoint_x = 0.0
        self.waypoint_y = -100 * map_scalar

        self.is_takeover = False
        self.is_evasive = False

    def setup_publisher(self):
        rospy.init_node('autopilot', anonymous=False)

        self.odom_pub = rospy.Publisher('boatodom', Marker, queue_size = 10)
        self.rate = rospy.Rate(30)

        self.sub = rospy.Subscriber('fr', String, self.callback)
        rospy.spin()

    def publish_me(self):
        msg = Marker()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = 'map'

        msg.pose.position = Point(self.me.coords[0], self.me.coords[1], 0.0)

        q = numpy.array([0.0, 0.0, 0.0, 0.0])

        msg.pose.orientation = Quaternion(*q)

        msg.type = Marker.SPHERE

        msg.scale.x = 60
        msg.scale.y = 60
        msg.scale.z = 60
        msg.color.a = 1.0
        msg.color.r = 0.0
        msg.color.g = 0.0
        msg.color.b = 1.0

        self.odom_pub.publish(msg)
        self.rate.sleep()

    def callback(self, data):
        if True:
            boatmsg_raw = ast.literal_eval(data.data)
            boatmsg = str(boatmsg_raw).strip('[]')

            try:
                self.objects = list(chain.from_iterable(boatmsg_raw)) #scanner
            except:
                self.objects = list(boatmsg_raw)

            if not self.is_takeover: #self boat movements
                if math.fabs(self.me.coords[1]) > 100 * map_scalar:
                    #self.me.angle = self.me.angle + math.pi
                    self.waypoint_y = self.waypoint_y * -1.0

                b = list(self.me.coords)

                if False: #self.is_evasive:
                    pass

                else:
                    delta_a = (self.waypoint_x - list(self.me.coords)[0])
                    delta_b = (self.waypoint_y - list(self.me.coords)[1])

                    if delta_b == 0.0:
                        delta_b = 0.0001

                    stupid_var = (map_scalar * 100 - self.waypoint_y) / (map_scalar * 100 * 2) - 1.0

                    self.me.angle = math.atan(delta_a / delta_b) + math.pi + math.pi * stupid_var

                    b[0] = b[0] + self.me.speed * math.sin(self.me.angle)
                    b[1] = b[1] + self.me.speed * math.cos(self.me.angle)

                for eb_raw in range(len(self.objects)/2): #scan boat relations
                    eb = eb_raw * 2

                    a = self.objects[eb] - b[0]
                    bas = self.objects[eb+1] - b[1]

                    c = math.sqrt(a*a + bas*bas)

                    if c < 300.0: #evasive maneuvers?
                        self.is_evasive = True
                    else:
                        self.is_evasive = False

                    if c < 45.0: #boat crashes?
                        print "OH NOOOO!!!"

                        print a, bas

                        b[1] = 100 * map_scalar

                        self.waypoint_y = -100 * map_scalar
                        #self.me.angle = math.pi

                self.me.coords = tuple(b)

            self.publish_me()

if __name__ == '__main__':
    try:
        coltrane = autopilot()
        coltrane.setup_publisher()

    except rospy.ROSInterruptException:
        pass

