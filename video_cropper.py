from PIL import Image
from moviepy.editor import VideoFileClip
import streamlit as st
import os



def get_frame_at_time(video_path, time_sec):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Get the frame at the given time (in seconds)
    frame = video_clip.get_frame(t=time_sec)

    # Close the video clip
    video_clip.close()

    return frame

def crop_video(video_path, output_path, x=None, y=None, width=None, height=None, start=None, end=None):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    if start is not None or end is not None:
        video_clip = video_clip.subclip(start, end)

    # Get original dimensions
    original_width, original_height = video_clip.size
    
    # Set default values if not provided
    if x is None:
        x = 0
    if y is None:
        y = 0
    if width is None:
        width = original_width
    if height is None:
        height = original_height

    # Crop the video
    cropped_clip = video_clip.crop(x1=x, y1=y, x2=x+width, y2=y+height)

    # Write the cropped video to the output file
    cropped_clip.write_videofile(output_path, codec='libx264', 
                     audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True,
                     logger=None
                     )

    # Close the video clips
    video_clip.close()
    cropped_clip.close()


def main():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    else:
        for file in os.listdir("tmp"):
            os.remove(os.path.join("tmp", file))
    st.title("Video Cropper")

    st.write("""
    This tool allows you to crop a video file to a specified region and time range.
    
    **Warning:** This is a basic version and may have bugs. 
    """)

    # Upload video file
    st.subheader("Upload Video File")
    uploaded_file = st.file_uploader("Upload video", type=["mp4", "mov"], key='video_cropper')

    if uploaded_file:
        # Display uploaded video path
        video_path = "tmp/uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.write("Uploaded Video Path:", video_path)
        # Get video duration using moviepy
        video_clip = VideoFileClip(video_path)
        duration = video_clip.duration
        # Get dimensions of the video
        video_width = video_clip.size[0]
        video_height = video_clip.size[1]
        wval = video_width // 2
        hval = video_height // 2

        dim = min(wval, hval)


        # Get parameters
        colms = st.columns(4)
        x = colms[0].number_input("X-coordinate of top-left corner (in pixels)", 
                                  value=video_width//2 - dim//2,
                                  min_value=0, max_value=video_width)
        y = colms[1].number_input("Y-coordinate of top-left corner (in pixels)", 
                                  value=video_height//2 - dim//2,
                                  min_value=0, max_value=video_height)
        width = colms[2].number_input("Width of cropped region (in pixels)", value=dim,         
                                      min_value=1, max_value=video_width)
        height = colms[3].number_input("Height of cropped region (in pixels)", value=dim,
                                        min_value=1, max_value=video_height)
        colms2 = st.columns(2)
        start = colms2[0].number_input("Start time (in seconds)", min_value=0.0)
        end = colms2[1].number_input("End time (in seconds)", 
                                     min_value=start if start is not None else 0.0, 
                                     max_value=duration, 
                                     value=min(start + 1., duration) if start is not None else 1.0
                                    )

        # Display video duration and dimensions
        st.write(f"Video Duration: {duration} seconds")
        st.write(f"Video Dimensions (H x W): {video_height} x {video_width} pixels")

        btn_colms = st.columns(2)

        # Display the video with a space on the right for previewing the cropped video
        col1, col2 = st.columns(2)
        with col1:
            st.video(video_path)

        if 'crop' not in st.session_state:
            st.session_state.crop = False
        if 'preview' not in st.session_state:
            st.session_state.preview = False

        def click_preview():
            st.session_state.preview = True

        
        with btn_colms[0]:
            should_crop = st.button("Preview Cropped Region", 
                                    on_click=click_preview)

        # Crop video
        if should_crop:
            cropped_frame = get_frame_at_time(video_path, start)
            cropped_frame = cropped_frame[y:y+height, x:x+width]
            # Display the cropped frame indicating the region in the second column
            with col2:
                st.write("Preview:")
                st.image(cropped_frame, use_column_width=True)

        if st.session_state.preview:
            confirm = btn_colms[1].button("Crop Video")
            
            if confirm:
                output_path = "tmp/cropped_video.mp4"
                crop_video(video_path, output_path, x=x, y=y, width=width, height=height, start=start, end=end)
                with col2:
                    st.success(f"Video cropped successfully! You can download the cropped video by clicking on the three dots on the right and selecting 'Download'.")
                
                    st.video(output_path)


if __name__ == "__main__":
    main()
