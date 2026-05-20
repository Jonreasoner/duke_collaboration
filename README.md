Readme file:

testing.py is the file you want to run. 

Edit testing.py to include the new trajectory. 

The output is the trajectory that a robot will take which is generated using A*. 

You get a cell by cell trajectory, sparse waypoints, and total length. 

grid is the world map, rooms is a dictionary that ties coordinates to features within the map... for example rooms["room_1"]["center"] returns the center grid cell for room 1 in (x,y) with (0,0) being the top left corner 