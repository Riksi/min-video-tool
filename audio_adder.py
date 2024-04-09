from moviepy.editor import VideoFileClip, AudioFileClip
import streamlit as st
import os

def add_audio_to_video(video_path, audio_path, output_path='output_video.mp4'):
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    if audio_clip.duration > video_clip.duration:
        audio_clip = audio_clip.subclip(0, video_clip.duration)

    # Set the audio of the video clip to the provided audio clip
    video_clip = video_clip.set_audio(audio_clip)

    # Write the video clip with the new audio to a file
    video_clip.write_videofile(output_path, codec='libx264', 
                     audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True,
                     logger=None
                     )
    # Close the video clip
    video_clip.close()
    return output_path

def main():
    # Clear tmp if it exists or create it
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    else:
        for file in os.listdir("tmp"):
            os.remove(os.path.join("tmp", file))
    st.title("Audio Addition")

    st.write("""
    A simple tool to add audio to a video file.
    
    **Warning:** This is a basic version and may have bugs.
    """)

    # Upload video file
    st.subheader("Upload Video File")
    uploaded_video_file = st.file_uploader("Upload video", type=["mp4", "mov"], key='audio_adder_video')
    uploaded_audio_file = st.file_uploader("Upload audio", type=["mp3", "wav"], key='audio_adder_audio')


    if uploaded_video_file and uploaded_audio_file:
        video_path = "tmp/uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_video_file.read())

        audio_path = "tmp/uploaded_audio.mp3"
        with open(audio_path, "wb") as f:
            f.write(uploaded_audio_file.read())

        st.video(video_path)
        st.audio(audio_path)

        if st.button("Add Audio"):
            output_path = add_audio_to_video(video_path, audio_path)
            st.success("Audio added successfully. You can download the video by clicking on the three dots on the right and selecting 'Download'.")
            st.video(output_path)









