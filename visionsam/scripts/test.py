#!/usr/bin/env python
f = open("/home/turtlebot/catkin_ws/src/visionsam/waypoints.txt", "r")
if f.mode == 'r':
    contents = f.read()
print contents

coords_raw = contents.split("position:")

print(coords_raw)
coords_raw = [elt.strip() for elt in coords_raw]
#elts_stripped = coords_raw.strip()
coords_pos = [elt.split('\t')]
print(coords_pos)
