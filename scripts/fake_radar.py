# fake radar for testing + pcl publisher
# big soda

import rospy
import random
from std_msgs.msg import String, Header
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import ast
from ast import literal_eval as make_tuple

class radar:
    def __init__(self):
        self.objects = []

        self.pub = rospy.Publisher('fr', String, queue_size=10)

        self.odom_pub = rospy.Publisher('odfr', PointCloud, queue_size=10)

        rospy.init_node('fakeradar', anonymous=False)
        self.rate = rospy.Rate(30)

        head = Header()
        head.stamp = rospy.Time.now()
        head.frame_id = 'map'

        self.cloudy = PointCloud()
        self.cloudy.header = head
        #self.cloudy.points = 10

    def callback(self, data):
        try:
            if True: #random.randint(0,3) == 1: #how bad radar is

                boatmsg = str(ast.literal_eval(data.data)).strip('[]')

                self.pub.publish(boatmsg)
                self.rate.sleep()

                dat = list(ast.literal_eval(data.data))

                self.cloudy.points = []

                for d in range(len(dat)): #move boats
                    point = Point()

                    try:
                        point.x, point.y = dat[d]
                    except:
                        point.x, point.y = dat

                    point.z = 0.0

                    self.cloudy.points.append(point)

                print self.cloudy.points[0]

                self.odom_pub.publish(self.cloudy)

        except:
            print "whooops"

    def receiver(self):
        rospy.Subscriber('fb', String, self.callback)

        rospy.spin()

if __name__ == '__main__':
    fakeNews = radar()

    try:
        fakeNews.receiver()

    except rospy.ROSInterruptException:
        pass

