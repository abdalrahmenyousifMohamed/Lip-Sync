import os
import time
import torch
import warnings
import configparser
import streamlit as st
from easy_functions import format_time, show_video

# Function to install requirements
def install_requirements():
    os.system("pip install -r requirements.txt")

# Function to setup and check prerequisites
def setup_and_prerequisites():
    # Check if GPU is enabled
    st.write('Checking for GPU or MPS...')
    if not (torch.cuda.is_available() or torch.backends.mps.is_available()):
        st.error('No GPU or MPS in runtime. Please ensure you have a GPU enabled.')
        return False

    if torch.cuda.is_available():
        st.write('CUDA GPU is available.')
    elif torch.backends.mps.is_available():
        st.write('MPS GPU is available.')

    # Create necessary directories
    os.makedirs('face_alignment', exist_ok=True)
    os.makedirs('temp', exist_ok=True)

    # Install prerequisites
    st.write('Installing batch_face...')
    warnings.filterwarnings("ignore", category=UserWarning, module='torchvision.transforms.functional_tensor')

    st.write('Fixing basicsr degradations.py')
    os.system("cp degradations.py /Users/pepo_abdo/Desktop/Lib-Sync/.venv/lib/python3.9/site-packages/basicsr/data/degradations.py")

    st.write('Installing gfpgan...')
    os.system("python install.py")

    st.success("Installation complete, move to Step 2!")
    return True

# Function to process video and audio
def process_video_and_audio(video_path, vocal_path, settings):
    # Start timer
    start_time = time.time()

    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Add settings to ConfigParser object
    config['OPTIONS'] = settings['options']
    config['PADDING'] = settings['padding']
    config['MASK'] = settings['mask']
    config['OTHER'] = settings['other']

    # Write the data to an INI file
    with open('config.ini', 'w') as f:
        config.write(f)

    # Run the main processing script
    os.system(f"python3 run.py")

    elapsed_time = time.time() - start_time
    st.write(f"Execution time: {format_time(elapsed_time)}")

    if settings['other']['preview_settings']:
        if os.path.isfile(os.path.join('temp', 'preview.jpg')):
            st.image(os.path.join('temp', 'preview.jpg'))
    else:
        if os.path.isfile(os.path.join('temp', 'output.mp4')):
            st.video(os.path.join('temp', 'output.mp4'))

# Function to save uploaded file
def save_uploaded_file(uploaded_file, directory="uploads"):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Streamlit app
def main():
    st.title("Audio-Video Synchronization App")

    # Input paths for video and audio files
    video_file = st.file_uploader("Upload Video File", type=["mp4"])
    vocal_file = st.file_uploader("Upload Audio File", type=["wav"])

    if video_file is not None and vocal_file is not None:
        # Save files and get paths
        video_path = save_uploaded_file(video_file, "uploaded_files")
        vocal_path = save_uploaded_file(vocal_file, "uploaded_files")

        st.write(f"Video file saved to: {video_path}")
        st.write(f"Audio file saved to: {vocal_path}")

        # Processing settings
        quality = st.selectbox("Select Quality", ["Fast", "Improved", "Enhanced"], index=2)
        output_height = st.selectbox("Select Output Height", ["half resolution", "full resolution", "480"], index=1)
        use_previous_tracking_data = st.checkbox("Use Previous Tracking Data", value=True)
        wav2lip_version = st.selectbox("Select Wav2Lip Version", ["Wav2Lip", "Wav2Lip_GAN"], index=0)
        nosmooth = st.checkbox("No Smooth", value=True)

        # Padding settings
        U = st.slider("Padding Up", -100, 100, 0)
        D = st.slider("Padding Down", -100, 100, 10)
        L = st.slider("Padding Left", -100, 100, 0)
        R = st.slider("Padding Right", -100, 100, 0)

        # Mask settings
        size = st.slider("Mask Size", 1.0, 6.0, 1.5)
        feathering = st.slider("Mask Feathering", 0, 3, 1)
        mouth_tracking = st.checkbox("Mouth Tracking", value=False)
        debug_mask = st.checkbox("Debug Mask", value=False)

        # Other settings
        batch_process = st.checkbox("Batch Process", value=False)
        output_suffix = st.text_input("Output Suffix", "Enhanced")
        include_settings_in_suffix = st.checkbox("Include Settings in Suffix", value=False)
        preview_input = st.checkbox("Preview Input", value=False)
        preview_settings = st.checkbox("Preview Settings", value=False)
        frame_to_preview = st.number_input("Number of FrameS to Preview", value=700)

        # Collect settings
        settings = {
            'options': {
                'video_file': video_path,
                'vocal_file': vocal_path,
                'quality': quality,
                'output_height': output_height,
                'wav2lip_version': wav2lip_version,
                'use_previous_tracking_data': use_previous_tracking_data,
                'nosmooth': nosmooth,
                'preview_window': 'Full'
            },
            'padding': {'U': U, 'D': D, 'L': L, 'R': R},
            'mask': {'size': size, 'feathering': feathering, 'mouth_tracking': mouth_tracking, 'debug_mask': debug_mask},
            'other': {
                'batch_process': batch_process,
                'output_suffix': output_suffix,
                'include_settings_in_suffix': include_settings_in_suffix,
                'preview_input': preview_input,
                'preview_settings': preview_settings,
                'frame_to_preview': frame_to_preview
            }
        }

        if st.button("Run"):
            with st.spinner("Processing..."):
                install_requirements()
                if setup_and_prerequisites():
                    process_video_and_audio(video_path, vocal_path, settings)

if __name__ == "__main__":
    main()