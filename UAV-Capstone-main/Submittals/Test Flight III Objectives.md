# Test Flight III Objectives

## Computer Vision Data Collection

- During several flights, the camera will be recording a live video feed to collect real-world data for further algorithm testing. When possible, the drone will takeoff from and land on the landing platform to provide in-frame video.

## Standard GPS Test

1. Position flight mode:
   - "Manual" controlled flight that relies on GPS for holding position.
   - Test RC control failsafe:
     - Different than previous tests; the drone should return to takeoff position.
2. Takeoff and Land:
   - Use python script to test takeoff and landing.
   - Record different between takeoff and landing positions (using a golf marker).
3. Mission Flight: 
   - Use python script to fly between predetermined waypoints, and land.
   - Record different between takeoff and landing positions (using a golf marker).
## GPS-RTK Test

1. Position flight mode:

   - "Manual" controlled flight that relies on GPS-RTK for holding position.

2. Takeoff and Land:

   - Use python script to test takeoff and landing.
   - Record different between takeoff and landing positions (using a golf marker).

3. Mission Flight: 

   - Use python script to fly between predetermined waypoints, and land.
   - Record different between takeoff and landing positions (using a golf marker).

4. Offboard Flights:

   - Test offboard flight controls, both from takeoff and mid-flight.

   - All offboard tests will be run in Gazebo prior to flight.

   - Will determine the relative coordinate plane in real-world flight vs Gazebo.

   - RTK will provide greater accuracy than standard GPS, reducing the risk of offboard mode.
## RTK-Altitude Data Source Test

- Barometer measurements are subject to noise from wind, rotor wash, pressure changes, and attitude changes. We have observed this during the first and second test flights. Further, this noise sometimes prohibits the switch to GPS-based flight.  The published, vertical accuracy of GPS-RTK for our receiver is a theoretical 0.01m. If relatively close to this value, GPS-RTK would become a very stable primary source of altitude information.
1. Repeat "GPS-RTK Test" flights with the GPS is selected as the primary source of altitude information.

## Step Input Response
- Log the drone's control response to a series of step changes of pitch, roll, and yaw through an offboard command. This will be compared to the Gazebo model and will serve as a repeatable benchmark for further tuning.