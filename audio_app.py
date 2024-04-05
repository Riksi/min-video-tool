from moviepy.editor import VideoFileClip
import streamlit as st
import os

def extract_audio(video_path, start_time, end_time, output_audio_path):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Extract the audio from the specified time range
    audio_clip = video_clip.subclip(start_time, end_time).audio

    # Write the audio clip to the output audio file
    audio_clip.write_audiofile(output_audio_path)

    return output_audio_path

def main():
    # Clear tmp if it exists or create it
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    else:
        for file in os.listdir("tmp"):
            os.remove(os.path.join("tmp", file))
    st.title("Audio Extractor")

    st.write("""
    This app allows you to extract audio from a video file.
    
    **Warning:** This is a basic version and may have bugs.         
    """)

    # Upload video file
    st.subheader("Upload Video File")
    uploaded_file = st.file_uploader("Upload video", type=["mp4"], key='audio_app')

    if uploaded_file:
        # Display uploaded video path
        video_path = "tmp/uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())
        st.write("Uploaded Video Path:", video_path)

        ## Display the video
        st.video(video_path)

        # Get parameters
        start_time = st.number_input("Start time (seconds)", min_value=0)
        end_time = st.number_input("End time (seconds)", min_value=start_time if start_time is not None else 0)
        
        output_audio_path = os.path.join("tmp/output_audio.mp3")

        # Extract audio
        if st.button("Extract Audio"):
            extract_audio(video_path, start_time, end_time, output_audio_path)
            # Delete the uploaded video file
            os.remove(video_path)
            st.success(f"Audio extracted successfully! You can download the audio file by clicking on the three dots on the right and selecting 'Download'.")
            # Show the audio to play
            st.audio(output_audio_path, format="audio/mp3")



if __name__ == "__main__":
    main()
