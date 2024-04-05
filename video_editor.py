import streamlit as st
import audio_app
import video_cropper
import video_merger
import image_sequence_video

tab1, tab2, tab3, tab4 = st.tabs(['Audio Extractor', 'Video Cropper', 'Video Merger',
                             "Image Sequence Video"])
with tab1:
    audio_app.main()

with tab2:
    video_cropper.main()

with tab3:
    video_merger.main()

with tab4:
    image_sequence_video.main()