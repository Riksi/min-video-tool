import streamlit as st
import audio_app
import video_cropper
import audio_adder

def hidden_error(e):
    print(e)
    st.error("An error occurred")

try:
    tab1, tab2, tab3 = st.tabs(['Audio Extractor', 'Video Cropper', 'Audio Adder'])
    with tab1:
        try:
            audio_app.main()
        except Exception as e:
            hidden_error(e)

    with tab2:
        try:
            video_cropper.main()
        except Exception as e:
            hidden_error(e)

    with tab3:
        try:
            audio_adder.main()
        except Exception as e:
            hidden_error(e)

except Exception as e:
    # Don't show the error message to the user
    hidden_error(e)
