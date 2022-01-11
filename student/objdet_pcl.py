# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Process the point-cloud and prepare it for object detection
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# general package imports
import cv2
import numpy as np
import torch

# add project directory to python path to enable relative imports
import os
import sys
import zlib
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# waymo open dataset reader
from tools.waymo_reader.simple_waymo_open_dataset_reader import utils as waymo_utils
from tools.waymo_reader.simple_waymo_open_dataset_reader import dataset_pb2, label_pb2

# object detection tools and helper functions
import misc.objdet_tools as tools

# Student imports
import open3d as o3d

def get_range_image(frame, lidar_name):
    # extract range image from frame
    lidar = [obj for obj in frame.lasers if obj.name == lidar_name][0] # get laser data structure from frame
    if len(lidar.ri_return1.range_image_compressed) > 0: # use first response
        ri = dataset_pb2.MatrixFloat()
        ri.ParseFromString(zlib.decompress(lidar.ri_return1.range_image_compressed))
        ri = np.array(ri.data).reshape(ri.shape.dims)
    return ri

WIND = None


# visualize lidar point-cloud
def show_pcl(pcl):

    ####### ID_S1_EX2 START #######     
    #######
    print("student task ID_S1_EX2")

    def update_wind(wind):
        wind.close()
        wind.poll_events()

    # step 1 : initialize open3d with key callback and create window
    global WIND
    first=False
    if WIND is None:
        first = True
    WIND = o3d.visualization.VisualizerWithKeyCallback()
    WIND.create_window()
    
    # step 2 : create instance of open3d point-cloud class
    pcd = o3d.geometry.PointCloud()

    # step 3 : set points in pcd instance by converting the point-cloud into 3d vectors (using open3d function Vector3dVector)
    pcl1 = pcl[:,:3]
    pcd.points = o3d.utility.Vector3dVector(pcl1)

    # step 4 : for the first frame, add the pcd instance to visualization using add_geometry; for all other frames, use update_geometry instead
    # if first:
    #     WIND.add_geometry(pcd)
    # else:
    #     WIND.add_geometry(pcd)
        #WIND.update_geometry(pcd)
    WIND.add_geometry(pcd)

    # step 5 : visualize point cloud and keep window open until right-arrow is pressed (key-code 262)
    WIND.register_key_callback(262, update_wind)
    WIND.run()
    
    
    #######
    ####### ID_S1_EX2 END #######     

# visualize range image
def show_range_image(frame, lidar_name):

    ####### ID_S1_EX1 START #######     
    #######
    print("student task ID_S1_EX1")

     # step 1 : extract lidar data and range image for the roof-mounted lidar
    ri = get_range_image(frame, lidar_name)
    
    # step 2 : extract the range and the intensity channel from the range image
    ri_range = ri[:,:,0]
    ri_intensity = ri[:,:,1]
    
    # step 3 : set values <0 to zero
    ri_range[ri_range<0] = 0.0
    ri_intensity[ri_intensity<0] = 0.0
    
    # step 4 : map the range channel onto an 8-bit scale and make sure that the full range of values is appropriately considered
    ri_range = ri_range * 255 / (np.amax(ri_range) - np.amin(ri_range)) 
    img_range = ri_range.astype(np.uint8)

    # step 5 : map the intensity channel onto an 8-bit scale and normalize with the difference between the 1- and 99-percentile to mitigate the influence of outliers
    lower_int_perc = np.percentile(ri_intensity,1)
    upper_int_perc = np.percentile(ri_intensity,99)
    ri_intensity[ri_intensity<=lower_int_perc] = lower_int_perc
    ri_intensity[ri_intensity>=upper_int_perc] = upper_int_perc
    ri_intensity = ri_intensity * 255 / (np.amax(ri_intensity) - np.amin(ri_intensity)) 
    img_intensity = ri_intensity.astype(np.uint8)

    # step 6 : stack the range and intensity image vertically using np.vstack and convert the result to an unsigned 8-bit integer
    img_range_intensity = np.vstack((img_range,img_intensity))
    img_range_intensity = img_range_intensity.astype(np.uint8)
    #######
    ####### ID_S1_EX1 END #######     
    
    return img_range_intensity

def scale_to_255(pcl):
    """
    Takes an arbitrary range and converts it to 0-255
    """
    pcl_min = pcl.min()
    pcl_max = pcl.max()
    scale_down = pcl - pcl.min()
    pcl_range = pcl_max - pcl_min
    scaled = (scale_down * (1/pcl_range * 255)).astype('uint8')
    return scaled


# create birds-eye view of lidar data
def bev_from_pcl(lidar_pcl, configs):

    # remove lidar points outside detection area and with too low reflectivity
    mask = np.where((lidar_pcl[:, 0] >= configs.lim_x[0]) & (lidar_pcl[:, 0] <= configs.lim_x[1]) &
                    (lidar_pcl[:, 1] >= configs.lim_y[0]) & (lidar_pcl[:, 1] <= configs.lim_y[1]) &
                    (lidar_pcl[:, 2] >= configs.lim_z[0]) & (lidar_pcl[:, 2] <= configs.lim_z[1]))
    lidar_pcl = lidar_pcl[mask]
    
    # shift level of ground plane to avoid flipping from 0 to 255 for neighboring pixels
    lidar_pcl[:, 2] = lidar_pcl[:, 2] - configs.lim_z[0]  

    # convert sensor coordinates to bev-map coordinates (center is bottom-middle)
    ####### ID_S2_EX1 START #######     
    #######
    print("student task ID_S2_EX1")

    ## step 1 :  compute bev-map discretization by dividing x-range by the bev-image height (see configs)
    x_range = (configs.lim_x[1] - configs.lim_x[0])
    discretization = x_range / configs.bev_height

    ## step 2 : create a copy of the lidar pcl and transform all metrix x-coordinates into bev-image coordinates    
    lidar_pcl_cp = lidar_pcl.copy()
    lidar_pcl_cp[:, 0] = np.int_(np.floor(lidar_pcl_cp[:, 0] / discretization))

    # step 3 : perform the same operation as in step 2 for the y-coordinates but make sure that no negative bev-coordinates occur
    y_range = (configs.lim_y[1] - configs.lim_y[0])
    discretization = y_range / configs.bev_width
    lidar_pcl_cp[:, 1] = np.int_(np.floor(lidar_pcl_cp[:, 1] / discretization))
    lidar_pcl_cp[:, 1] = scale_to_255(lidar_pcl_cp[:, 1])

    # step 4 : visualize point-cloud using the function show_pcl from a previous task
    #show_pcl(lidar_pcl_cp)
    
    #######
    ####### ID_S2_EX1 END #######     
    
    
    # Compute intensity layer of the BEV map
    ####### ID_S2_EX2 START #######     
    #######
    print("student task ID_S2_EX2")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    intensity_map = np.zeros(shape=(configs.bev_height+ 1, configs.bev_width+ 1))

    # step 2 : re-arrange elements in lidar_pcl_cpy by sorting first by x, then y, then -z (use numpy.lexsort)
    idx = np.lexsort((-lidar_pcl_cp[:, 3], lidar_pcl_cp[:, 1], lidar_pcl_cp[:, 0]))
    lidar_pcl_cp_intensity = lidar_pcl_cp[idx]

    ## step 3 : extract all points with identical x and y such that only the top-most z-coordinate is kept (use numpy.unique)
    ##          also, store the number of points per x,y-cell in a variable named "counts" for use in the next task
    _, idx, counts = np.unique(lidar_pcl_cp_intensity[:, 0:2], axis=0, return_index=True, return_counts=True)
    lidar_pcl_cp_intensity = lidar_pcl_cp_intensity[idx]

    ## step 4 : assign the intensity value of each unique entry in lidar_top_pcl to the intensity map 
    ##          make sure that the intensity is scaled in such a way that objects of interest (e.g. vehicles) are clearly visible    
    ##          also, make sure that the influence of outliers is mitigated by normalizing intensity on the difference between the max. and min. value within the point cloud
    intensity_map[np.int_(lidar_pcl_cp_intensity[:, 0]), np.int_(lidar_pcl_cp_intensity[:, 1])] = lidar_pcl_cp_intensity[:, 3]# / (np.amax(lidar_pcl_cp_intensity[:, 3])#-np.amin(lidar_pcl_cp_intensity[:, 3]))
    intensity_map[intensity_map > 1.0] = 1.0 # only one value over 1
    # print(np.histogram(intensity_map))

    ## step 5 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    show = False
    if show:
        img_intensity = scale_to_255(intensity_map)
        while (1):
            cv2.imshow('img_intensity', img_intensity)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    #######
    ####### ID_S2_EX2 END ####### 


    # Compute height layer of the BEV map
    ####### ID_S2_EX3 START #######     
    #######
    print("student task ID_S2_EX3")

    ## step 1 : create a numpy array filled with zeros which has the same dimensions as the BEV map
    height_map = np.zeros(shape=(configs.bev_height+ 1, configs.bev_width+ 1))

    ## step 2 : assign the height value of each unique entry in lidar_top_pcl to the height map 
    ##          make sure that each entry is normalized on the difference between the upper and lower height defined in the config file
    ##          use the lidar_pcl_top data structure from the previous task to access the pixels of the height_map
    height_map[np.int_(lidar_pcl_cp_intensity[:, 0]), np.int_(lidar_pcl_cp_intensity[:, 1])] = lidar_pcl_cp_intensity[:, 2] / float(np.abs(configs.lim_z[1] - configs.lim_z[0]))

    ## step 3 : temporarily visualize the intensity map using OpenCV to make sure that vehicles separate well from the background
    show = False
    if show:
        img_height = scale_to_255(height_map)
        while (1):
            cv2.imshow('img_height', img_height)
            if cv2.waitKey(10) & 0xFF == 27:
                break
    #######
    ####### ID_S2_EX3 END #######       

    # Set changed variable names
    lidar_pcl_cpy = lidar_pcl_cp
    lidar_pcl_top = lidar_pcl_cp_intensity
    # height_map = []
    # intensity_map = []

    # Compute density layer of the BEV map
    density_map = np.zeros((configs.bev_height + 1, configs.bev_width + 1))
    _, _, counts = np.unique(lidar_pcl_cpy[:, 0:2], axis=0, return_index=True, return_counts=True)
    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(64)) 
    density_map[np.int_(lidar_pcl_top[:, 0]), np.int_(lidar_pcl_top[:, 1])] = normalizedCounts
        
    # assemble 3-channel bev-map from individual maps
    bev_map = np.zeros((3, configs.bev_height, configs.bev_width))
    bev_map[2, :, :] = density_map[:configs.bev_height, :configs.bev_width]  # r_map
    bev_map[1, :, :] = height_map[:configs.bev_height, :configs.bev_width]  # g_map
    bev_map[0, :, :] = intensity_map[:configs.bev_height, :configs.bev_width]  # b_map

    # expand dimension of bev_map before converting into a tensor
    s1, s2, s3 = bev_map.shape
    bev_maps = np.zeros((1, s1, s2, s3))
    bev_maps[0] = bev_map

    bev_maps = torch.from_numpy(bev_maps)  # create tensor from birds-eye view
    input_bev_maps = bev_maps.to(configs.device, non_blocking=True).float()
    return input_bev_maps


