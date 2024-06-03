import os
import shutil

import cv2
import numpy as np
import pyrealsense2 as rs

bag_file = "/Users/adiad/Documents/GitHub/realsense_bag_reader/walk1/walk1.bag"
frame_dir = "/Users/adiad/Documents/GitHub/realsense_bag_reader/walk1/frames"
start_sec = 2
end_sec = 36
n_out_frames = 200

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, bag_file, repeat_playback=False)
    # Configure the pipeline to stream the depth stream
    # valid formats: 'any', 'bgr8', 'bgra8', 'combined_motion', 'disparity16', 'disparity32', 'distance', 'fg', 'gpio_raw', 'invi', 'inzi', 'm420', 'mjpeg', 'motion_raw', 'motion_xyz32f', 'name', 'raw10', 'raw16', 'raw8', 'rgb8', 'rgba8', 'six_dof', 'uyvy', 'value', 'w10', 'xyz32f', 'y10bpack', 'y12i', 'y16', 'y16i', 'y411', 'y8', 'y8i', 'yuyv', 'z16', 'z16h'
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.z16, 30)
    fps = 30
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, fps)

    # loop through video frames to get all frame numbers
    is_frame = True
    frame_nums = []
    profile = pipeline.start(config)
    # Needed so frames don't get dropped during processing:
    profile.get_device().as_playback().set_real_time(False)
    while is_frame:
        is_frame, frame = pipeline.try_wait_for_frames()
        if is_frame:
            frame_nums += [frame.frame_number]
    pipeline.stop()
    
    # find the frame numbers to save
    frame_nums = frame_nums[start_sec*fps:end_sec*fps]
    n_frames = len(frame_nums)
    stride = int(n_frames/n_out_frames)
    out_frames = frame_nums[::stride]

    # setup output directory
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    os.makedirs(frame_dir)

    is_frame = True
    profile = pipeline.start(config)
    # Needed so frames don't get dropped during processing:
    profile.get_device().as_playback().set_real_time(False)
    while is_frame:
        is_frame, frame = pipeline.try_wait_for_frames()
        if is_frame:
            if frame.frame_number in out_frames:

                # Get image frame
                image = frame.get_color_frame()

                # Convert image_frame to rightside up bgr numpy array to render image in opencv from upside down rgb
                image = np.asanyarray(image.get_data())[:, :, ::-1][::-1,::-1]
                cv2.imwrite(f"{frame_dir}/{frame.frame_number:09}.jpg", image)
    pipeline.stop()

finally:
    pass