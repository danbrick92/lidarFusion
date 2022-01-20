# Writeup - Part 2 - Sensor Fusion and Tracking
## Part 1
### Instructions
Write a short recap of the four tracking steps and what you implemented there (EKF, track management, data association, camera-lidar sensor fusion). Which results did you achieve? Which part of the project was most difficult for you to complete, and why?

### EKF
In the EKF stage, I implemented the Extended Kalman Filter equations. These equations are built out into two phases: the predict and update phase. 

#### Predict Phase
In the predict phase, we take the current state and estimate where we think the new state will be. In order to achieve this, we need to transform the state with a state transition matrix F. 

We also need to update our estimation error covariance matrix P by also applying the state transition matrix to it, as well as adding Q (which accounts for changes in acceleration like braking and speeding up).

#### Update Phase
In the update phase, we take the current track and factor in a new measurement. This has the effect of lowering the uncertainty overall.

In order to do this, we first need to create gamma. Gamma compares the new measurement (called z) with a state estimation H (or h(x) which is non-linear) applied to x, our current state. In other words, our measurement z is in image coordinates. We use hx to transform x (our current state), into those same coordinates. We then subtract z from hx, giving us the different between our prediction and the measurement

We also have to create matrix S. This matrix converts the error covariance matrix P to measurement coordinates, and then adds R which is the measurement noise matrix. S gives us the overall uncertainty.

Next we create matrix K, the Kalman Gain. THis is the Error Covariance matrix, changed to measurement coordinates, multiplied with the inverse of the overall uncertainty S. It gives us the weights of our predictions vs. measurement.

We then add to our original state X the Kalman Gain K multiplied with gamma. This essentially updates x with the residual gamma, weighted by the Kalman Gain. 

Finally, we change our P error covariance matrix by basically multiplying it with our Kalman Gain. In practice, to do this we need to take the Identity matrix I and subtract from it K*H. 

### Track Management
In the track management module, we implemented a system for keeping track of different measurement scores. This system allows the self-driving car to build confidence over time when it continually sees the same car over and over. It helps eliminate false positives by setting a score threshold, which basically means the car needs to be seen a certain consecutuve number of times before being tracked. It also helps remove cars that have left the FOV by removing them based on the score.

### Association
The association system attributes measurements to tracks. It does this by using the Mahalanobis distance, which factors both positional different and uncertainty into the equation. These distances are tracked in an association matrix, with N tracks and M measurements. When a track and measurement are matched (found via min distance), they are both removed from the association matrix. 

Remaining tracks are passed on to the track management system and penalized in terms of track score.

### Camera-Lidar Sensor Fusion
This part of the projetc dealt with supporting camera measurements. Most importantly, this dealt with implementing the function h(x), the non-linear function that transforms coordinates to image coordinates. 

### Results
The results were very successful! All of the vehicles in the frames 0-200 of sequence 1 were found with RMSE's of below .2!

### Most Difficult
I had the most difficulty implementing the Camera-Lidar Sensor Fusion part of this project. The reason is because I did not have my H() function created in a way that supported camera coordinates. Since this was the last portion of the assignment, I had a hard time locating where the problem was. It took me some time before I realized it was the EKF H() function that was wrong. 

## Part 2
Do you see any benefits in camera-lidar fusion compared to lidar-only tracking (in theory and in your concrete results)?

I saw benefits of the fusion both in theory and in tracking. 

In theory, LIDAR and Camera have different pros and cons. LIDAR is good at judging distances from other vehicles, and is a dynamic sensor that is not subject to lighting conditions. On the other hand, it suffers from low reflectivity and does not do as good of a job on it's own with classification. Camera on the other hand is great with classification, but does a poor job with depth perception. By combining both systems, we take advantage of the pros of these components and significantly reduce the cons. 

In practice, I found that my system identified far less false positives than LIDAR alone. There were quite a few frames where LIDAR thought a bush was a car for a few frames. The camera did not see this. Because the camera was fused, it was able to discount this false positive.

## Part 3
Which challenges will a sensor fusion system face in real-life scenarios? Did you see any of these challenges in the project?

I imagine one of the toughest challenges to deal with is calibration. In sensor fusion, it is required to be able to shift the sensor coordinates to the same coordinate system. If the calibration isn't spot on, it's going to fail. I did not see this in my system.

Another situation that causes issues are different environmental conditions. What happens if the scene is completely dark? The camera will not see anything, but the LIDAR will see a lot. If these systems do not agree, the current fusion setup will essentially discount the LIDAR senses because the camera doesn't agree. The opposite could be true if it's raining or snowing: the LIDAR sensor could surface false positives. There needs to be a mechanism to evaluate environmental conditions to perhaps weight the sensors in one favor or another. I did not experience this in the project.

## Part 4
Can you think of ways to improve your tracking results in the future?

For one, implementing something beyond the Simple Nearest Neighbor association method should work better. It's possible in the current system to associate measurements inappropriately because they are not globally optimum.

Another way to improve tracking results is to fine tune the YOLO network. Spend more time training the network to better recognize LIDAR and camera images. 

The current scoring system I have is also quite limited. I could think of a more smoothed system that discounts track score more the less they are caught by our sensors. 

## RMSE Images
### Part 1
![Part 1](img/RMSE_Step_1.png?raw=true)<br>

### Part 2
![Part 2](img/RMSE_Step_2.png?raw=true)<br>

### Part 3
![Part 3](img/RMSE_Step_3.png?raw=true)<br>

### Part 4
![Part 4](img/RMSE_Step_4.png?raw=true)<br>

## RMSE Video
The video is located in results/my_tracking_results.7z. You can uncompress it and then play the avi. 