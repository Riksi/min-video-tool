import cv2
import streamlit as st
import os

def concatenate_videos(video_paths, output_path):
    # Read videos
    videos = [cv2.VideoCapture(path) for path in video_paths]

    # Get properties of the first video
    width = int(videos[0].get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(videos[0].get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(videos[0].get(cv2.CAP_PROP_FPS))

    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write frames from each video to output video
    for video in videos:
        while True:
            ret, frame = video.read()
            if not ret:
                break
            out.write(frame)

    # Release VideoCapture and VideoWriter objects
    for video in videos:
        video.release()
    out.release()

def main():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    else:
        for file in os.listdir("tmp"):
            os.remove(os.path.join("tmp", file))
    st.title("Video Merger")

    st.write("""
    This app allows you to merge multiple videos into a single video file.
    
    **Warning:** This is a basic version and may have bugs. Ensure that all videos have the same dimensions and frame rates. 
    
    """)

    # Upload video files
    st.subheader("Upload Video Files")
    st.write("Upload the videos in the order you want them to be concatenated.")
    uploaded_files = st.file_uploader("Upload videos", type=["mp4"], accept_multiple_files=True)

    if uploaded_files:
        st.write("The videos will be merged in the following order:")
        st.write(", ".join([file.name for file in uploaded_files]))
        # Display uploaded video paths
        video_paths = [f"tmp/video_{i}.mp4" for i, file in enumerate(uploaded_files, start=1)]
        for file, video_path in zip(uploaded_files, video_paths):
            with open(video_path, "wb") as f:
                f.write(file.read())
        # Get output video save path
        output_path = "tmp/output_video.mp4"

        # Concatenate videos
        if st.button("Merge Videos"):
            concatenate_videos(video_paths, output_path)
            st.success(f"Videos concatenated successfully! You can download the concatenated video by clicking on the button below.")
            st.download_button(label="Download Concatenated Video", data=open(output_path, 'rb'), file_name='output_video.mp4', mime='video/mp4',
                                 key="download_merged_video")

if __name__ == "__main__":
    main()
