#####################################################
##               Read bag from file                ##
#####################################################


# First import library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
# Import argparse for command-line options
import argparse
# Import os.path for file path manipulation
import os.path

# # Create object for parsing command-line options
# parser = argparse.ArgumentParser(description="Read recorded bag file and display depth stream in jet colormap.\
#                                 Remember to change the stream resolution, fps and format to match the recorded.")
# # Add argument which takes path to a bag file as an input
# parser.add_argument("-i", "--input", type=str, help="Path to the bag file")
# # Parse the command line arguments to an object
# args = parser.parse_args()
# # Safety if no parameter have been given
# if not args.input:
#     print("No input paramater have been given.")
#     print("For help type --help")
#     exit()
# # Check if the given file have bag extension
# if os.path.splitext(args.input)[1] != ".bag":
#     print("The given file is not of correct file format.")
#     print("Only .bag files are accepted")
#     exit()
try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()
    # Tell config that we will use a recorded device from filem to be used by the pipeline through playback.
    rs.config.enable_device_from_file(config, "/Users/adiad/Documents/GitHub/realsense_bag_reader/20240508_132505.bag")
    # Configure the pipeline to stream the depth stream
    # valid formats: 'any', 'bgr8', 'bgra8', 'combined_motion', 'disparity16', 'disparity32', 'distance', 'fg', 'gpio_raw', 'invi', 'inzi', 'm420', 'mjpeg', 'motion_raw', 'motion_xyz32f', 'name', 'raw10', 'raw16', 'raw8', 'rgb8', 'rgba8', 'six_dof', 'uyvy', 'value', 'w10', 'xyz32f', 'y10bpack', 'y12i', 'y16', 'y16i', 'y411', 'y8', 'y8i', 'yuyv', 'z16', 'z16h'
    # config.enable_stream(rs.stream.color, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)


    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render image in
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    
    # Create colorizer object
    colorizer = rs.colorizer();
    out = cv2.VideoWriter('/Users/adiad/Documents/GitHub/realsense_bag_reader/test.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1280,720))

    # Streaming loop
    last_frame_number = 0
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()
        if frames.frame_number < last_frame_number:
            break

        # Get depth frame
        # depth_frame = frames.get_depth_frame()
        # print(dir(frames))
        depth_frame = frames.get_color_frame()

        # Colorize depth frame to jet colormap
        # depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_frame.get_data())[:, :, ::-1] # rgb to bgr
        out.write(depth_color_image)

        # Render image in opencv window
        cv2.imshow("Depth Stream", depth_color_image)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break
        last_frame_number = frames.frame_number

finally:
    pass