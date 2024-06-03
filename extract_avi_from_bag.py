import pyrealsense2 as rs
import numpy as np
import cv2

bag_file = "/Users/adiad/Documents/GitHub/realsense_bag_reader/20240508_132505.bag"
avi_file = "/Users/adiad/Documents/GitHub/realsense_bag_reader/test.avi"

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, bag_file)
    # Configure the pipeline to stream the depth stream
    # valid formats: 'any', 'bgr8', 'bgra8', 'combined_motion', 'disparity16', 'disparity32', 'distance', 'fg', 'gpio_raw', 'invi', 'inzi', 'm420', 'mjpeg', 'motion_raw', 'motion_xyz32f', 'name', 'raw10', 'raw16', 'raw8', 'rgb8', 'rgba8', 'six_dof', 'uyvy', 'value', 'w10', 'xyz32f', 'y10bpack', 'y12i', 'y16', 'y16i', 'y411', 'y8', 'y8i', 'yuyv', 'z16', 'z16h'
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)

    out = cv2.VideoWriter(avi_file, cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1280, 720))

    # Start streaming from file
    last_frame_number = 0
    pipeline.start(config)

    # Streaming loop
    while True:
        # Get frameset
        frames = pipeline.wait_for_frames()

        # Escape the loop when frame number resets to first frame
        if frames.frame_number < last_frame_number:
            break

        # Get image frame
        image_frame = frames.get_color_frame()

        # Convert image_frame to bgr numpy array to render image in opencv from rgb
        depth_color_image = np.asanyarray(image_frame.get_data())[:, :, ::-1]
        out.write(depth_color_image)

        last_frame_number = frames.frame_number

finally:
    pass