# Writeup - Point Cloud
## Part 1: Vehicle Examples
Find and display 6 examples of vehicles with varying degrees of visibility in the point-cloud
<br>
### Good Visibility
#### Car 1
Car 1 is outside the immediate vicinity of the roof and the blind spots of the top LIDAR. There is nothing occluding the car, which gives a great result. <br>
![Car Great 1](img/report_car_great_1.png?raw=true)
<br>
#### Car 2
Car 2 is much farther from the LIDAR sensing vehicle, yet it gives us a clear idea that this a van with a ladder on the roof. <br>
![Car Great 2](img/report_car_great_2.png?raw=true)
<br>
#### Car 3
Car 3 is behind us, and we get a very clear picture about the type of vehicle it is, even to the point where we can see it's mirrors. <br> 
![Car Great 3](img/report_car_great_3.png?raw=true)
<br>
#### Car 4
Car 4 is in front of us, and we get a very dense clear picture of the rear bumper of the vehicle. <br> 
![Car Great 4](img/report_car_great_4.png?raw=true)
<br>
### Mediocre Visibility
#### Car 5
Car 5 is directly next to our current vehicle. We get a good sense of the car's upper shape, but it's lower shape is hidden due to blind spots. This gives a clear picture about why we need other LIDAR sensors postioned around the car. <br>
![Car Ok 1](img/report_car_ok_1.png?raw=true)
<br>
#### Car 6
Car 6 is quite far from our car, and from what I can gather is parked in a lot. You can see that the side of the vehicle facing the LIDAR sensing is quite evident. On the other hand, most notably the top of the vehicle is totally missing. <br>
![Car Ok 2](img/report_car_ok_2.png?raw=true)
#### Car 7
Car 7 is also quite far from our car, and is in front of a line of other cars. While the details of the rear bumper are fairly clear, it is difficult to determine any other features of the car. <br>
![Car Ok 2](img/report_car_ok_3.png?raw=true)
<br>
### Poor Visibility
#### Car 8
Car 8 is at the farthest reaches of the data. While you can make out that this object is a car, it is very poorly constructed. This helps show the limits of the LIDAR sensor. <br>
![Car Bad 1](img/report_car_bad_1.png?raw=true)
<br>
#### Car 9
Car 9 is actually directly next to the sensing vehicle. While the pickup truck itself is decently displayed, the trailer it is carying is not well constructed due to it being in the blind spot of the LIDAR top sensor. This, again, shows why we need to have multiple LIDAR sensors. <br>
![Car Bad 2](img/report_car_bad_2.png?raw=true)<br>
#### Car 10
Car 10 is quite far away, behind us. While it could be made out to be a car, there is also a pole that appears to be jutting out of the roof. It's discernable that this is part of the median strip, but only because of the color of the pole. In general, this vehicle is hard to recognize. <br>
![Car Bad 3](img/report_car_bad_3.png?raw=true)<br>
<br>
## Part 2: Features
### Overview
Identify vehicle features that appear as a stable feature on most vehicles (e.g. rear-bumper, tail-lights) and describe them briefly. Also, use the range image viewer from the last example to underpin your findings using the lidar intensity channel.<br>
<br>
The stability of these features highly depends on the direction of the vehicle. <br>
<br>
### Oncoming Traffic
With oncoming traffic, the hood and front-bumper of the vehicle are very stable. You can see an example of this on the LIDAR intensity image marked in blue.<br>
![Oncoming Side](img/report_oncoming_side.png?raw=true)
<br>
### Current Lane of Traffic
The opposite tends to be true of the traffic the sensing vehicle is driving with: we see back bumpers, left-sides. You can see an example of this on the LIDAR intensity image marked in red.<br>
![Current Side](img/report_our_side.png?raw=true)
<br>
### Windows
On the whole, it does appear like windows tend to not show up since they are a transparent surface. <br>
You can see an example of this on the LIDAR intensity image marked in green.<br>
![Windows](img/report_windows.png?raw=true)
<br>
### LIDAR Intensity Image
In this LIDAR intensity image, I show the correlaries to the above comments.<br>
![Intensity](img/report_range_intensity.png?raw=true)
<br>
