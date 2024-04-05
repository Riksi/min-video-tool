import cv2
import numpy as np
import streamlit as st
import os

def create_video(image_list, output_path='output_video.mp4', fps=60, duration_per_img=1):
    # Get dimensions of the first image
    height, width, _ = image_list[0].shape

    # Define codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Write images to video
    for img in image_list:
        for _ in range(int(fps * duration_per_img)):
            out.write(img)

    # Release VideoWriter object
    out.release()
    return output_path

def main():
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    else:
        for file in os.listdir("tmp"):
            os.remove(os.path.join("tmp", file))

    
    st.title("Image Sequence to Video")

    st.write("""
    This tool allows you to create a video from a sequence of images.
            
    **Warning:** This is a basic version and may have bugs.
    """)

    # Upload image files
    st.subheader("Upload Image Files")
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "png"], accept_multiple_files=True)

    if uploaded_files:
        # Display uploaded images
        images = [cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)[..., :3] for file in uploaded_files]

        # Display in rows of 5
        num_images = len(images)
        num_rows = int(np.ceil(num_images / 5))
        for i in range(num_rows):
            st.image([i[..., ::-1] for i in images[i*5:(i+1)*5]], width=150)


        # Get parameters
        #fps = st.number_input("Frames per second (FPS)", min_value=1, max_value=30, value=1)
        duration_per_img = st.number_input("Duration per image (seconds)", min_value=1, max_value=10, value=1)

        # Create video
        if st.button("Create Video"):
            output_path = create_video(images, fps=60, duration_per_img=duration_per_img)
            st.success(f"Video created successfully! You can download the video by clicking on the button below.")
            with open(output_path, "rb") as f:
                st.download_button("Download Video",
                                      f,
                                      file_name='output_video.mp4',
                                      mime='video/mp4',
                                    key="download_image_video")
                                   

if __name__ == "__main__":
    main()
