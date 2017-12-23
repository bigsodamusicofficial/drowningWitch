# drowningWitch
Autonomy and boats!

So far, the only thing in this beautiful repo is a boat swarm simulator. But it's a lot of fun to look at in rviz! Here's how you can try it:

1. Get them ros juices flowing:

```
roscore
```

2. Now in a new terminal, let's get our friend rviz into the picture:

```
cd /drowningWitch
rosrun rviz rviz -d sea.rviz
```

3. Wow! Look at that fantastic config! Okay, now let's crack open a cold can of boating simulation. In a new terminal:

```
cd /drowningWitch/scripts
python fake_boats.py
```

4. Superb! You're doing great. The following script subscribes to our boat spammer we just started and publishes it as radar. New terminal time:

```
cd /drowningWitch/scripts
python fake_radar.py
```

5. Now rviz should have some little white balls runnin' every which way like a scene outta Lord of the Flies. Now we can start our main boat simulator (and don't forget to grab yourself yet another terminal):

```
cd /drowningWitch/scripts
python autopilot.py
```

6. Bam! We should see a blue thing walking back and forth laterally across the map. The autopilot is pretty stupid right now; the only thing it can do is recognize the fact it's bumped into a boat. Have fun!
