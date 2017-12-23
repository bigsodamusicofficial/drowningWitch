
# fake boat spawner for testing radar
# big soda

import math
import rospy
import random
from std_msgs.msg import String

map_scalar = 4.0

class boat:
    def __init__(self):
        if random.randint(0,1) == 0:
            self.coords = ((random.randint(0,1)-0.5)*200*map_scalar, random.uniform(-100*map_scalar,100*map_scalar))
        else:
            self.coords = (random.uniform(-100*map_scalar,100*map_scalar), -100*map_scalar)

        self.turn_speed = 0.01 + random.uniform(0, 10) / 1000
        self.speed = 0.1 + random.uniform(0, 100) / 10
        self.angle = random.random() * math.pi * 2.0

        self.waypoint = self.angle

        self.sway = 0.0

class random_boats:
    def __init__(self):
        self.allboats = []

        self.msgs = []

        self.pub = rospy.Publisher('fb', String, queue_size=10)
        rospy.init_node('fakeboats', anonymous=False)
        self.rate = rospy.Rate(15)

    def boat_slinger(self):
        self.allboats.append(boat())

        while not rospy.is_shutdown():
            if random.randint(0,80) == 1:
                self.allboats.append(boat())
                print "NEEEEEEEWBOOOOOOOAAAAAAT!!!!!!!!!!"

            if len(self.allboats) == 0:
                continue

            for btnum in range(len(self.allboats)):
                bt = self.allboats[btnum]
                b = list(bt.coords)

                if random.randint(0, 90) == 1: #decides to turn
                    bt.waypoint = bt.waypoint + random.uniform(0, math.pi*2)
                    bt.sway = (random.randint(0,1) - 0.5)*2

                if random.randint(0, 90) == 1: #decides to change speed
                    self.speed = 0.1 + random.uniform(0, 100) / 10

                if math.fabs(bt.angle-bt.waypoint) > 0.035:
                    bt.angle = bt.angle + bt.turn_speed * bt.sway

                b[0] = b[0] + bt.speed * math.sin(bt.angle)
                b[1] = b[1] + bt.speed * math.cos(bt.angle)

                bt.coords = tuple(b)

                if math.fabs(b[0]) > 100 * map_scalar:
                    del self.allboats[btnum]
                    print "bam!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    break

                if math.fabs(b[1]) > 100 * map_scalar:
                    del self.allboats[btnum]
                    print "bam!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    break

            msg = str([b.coords for b in self.allboats]).strip('[]')
            rospy.loginfo(msg)
            self.pub.publish(msg)
            self.rate.sleep()

if __name__ == '__main__':
    fakeBoats = random_boats()

    try:
        fakeBoats.boat_slinger()
    except rospy.ROSInterruptException:
        pass

