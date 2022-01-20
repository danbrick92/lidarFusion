# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Kalman filter class
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import misc.params as params 

class Filter:
    '''Kalman filter class'''
    def __init__(self):
        
        pass

    def F(self):
        ############
        # Step 1: implement and return F
        ############
        dt = params.dt
        F = np.matrix([
            [1, 0, 0, dt, 0, 0],
            [0, 1, 0, 0, dt, 0],
            [0, 0, 1, 0, 0, dt],
            [0, 0, 0, 1, 0,  0],
            [0, 0, 0, 0, 1,  0],
            [0, 0, 0, 0, 0,  1]
        ])
        return F
        
        ############
        # END student code
        ############ 

    def Q(self):
        ############
        # Step 1: implement and return process noise covariance Q
        ############
        q = params.q
        dt = params.dt
        a = ((dt**3)/3) * q 
        b = ((dt**2)/2) * q 
        c = dt * q 
        Q = np.array([ 
            [a, 0, 0, b, 0, 0],
            [0, a, 0, 0, b, 0],
            [0, 0, a, 0, 0, b],
            [b, 0, 0, c, 0, 0],
            [0, b, 0, 0, c, 0],
            [0, 0, b, 0, 0, c]
        ])
        return Q
        
        ############
        # END student code
        ############ 

    def predict(self, track):
        ############
        # Step 1: predict state x and estimation error covariance P to next timestep, save x and P in track
        ############
        # Get variables
        x = track.x
        P = track.P
        F = self.F()
        Q = self.Q()

        # Calculations
        x = F.dot(x)
        P = F.dot(P).dot(F.T) + Q
        
        # Set Attributes
        track.set_x(x)
        track.set_P(P)

        ############
        # END student code
        ############ 

    def update(self, track, meas):
        ############
        # Step 1: update state x and covariance P with associated measurement, save x and P in track
        ############
        # Get variables
        z = meas.z
        x = track.x
        H = meas.sensor.get_H(x)
        P = track.P
        R = meas.R
        I = np.identity(params.dim_state)
        
        # Calculations
        gamma = self.gamma(track, meas)
        S = self.S(track, meas, H)
        K = P.dot(H.T).dot(np.linalg.inv(S))
        x = x + K.dot(gamma)
        P = (I - K.dot(H)).dot(P)

        # Set Attributes
        track.set_x(x)
        track.set_P(P)
        ############
        # END student code
        ############ 
        track.update_attributes(meas)
    
    def gamma(self, track, meas):
        ############
        # Step 1: calculate and return residual gamma
        ############
        z = meas.z
        x = track.x
        H = meas.sensor.get_hx(x)

        gamma = z - H
        return gamma        
        ############
        # END student code
        ############ 

    def S(self, track, meas, H):
        ############
        # Step 1: calculate and return covariance of residual S
        ############
        P = track.P
        R = meas.R

        S = H.dot(P).dot(H.T) + R
        return S
        
        ############
        # END student code
        ############ 