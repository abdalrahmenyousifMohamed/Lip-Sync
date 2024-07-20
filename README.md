
# Lip Sync Application

Wav2Lip is an advanced lip-syncing model designed to synchronize mouth movements with audio. Its primary strength lies in creating realistic and accurate lip movements, making it ideal for various applications in video editing and content creation

## Table of Contents

- Installation
- Configuration
- Usage
- Demo
- Project Structure

# Notes
- move degradations.py in the project files with exisiting one at basicsr/data/degradations.py to overwite and solve library issue

  ``` ! cp Lib/degradations.py $(python3 -m site --user-site)/basicsr/data/degradations.py ```

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/abdalrahmenyousifMohamed/Lip-Sync.git
    cd Lip-Sync
    ```

1.1 Create a virtual environment and activate it:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    
2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Update the `config.ini` file with your video and audio file paths and other settings. Here is an example configuration:

-   should experiment with different values to find the best balance for your clip
```ini
[OPTIONS]
video_file = /path/to/video.mp4
vocal_file = /path/to/audio.wav
quality = Enhanced
output_height = full resolution
wav2lip_version = Wav2Lip
use_previous_tracking_data = True
nosmooth = True
preview_window = Full

[PADDING]
U = 0
D = 10
L = 0
R = 0

[MASK]
size = 1.5
feathering = 1
mouth_tracking = False
debug_mask = False

[OTHER]
batch_process = False
output_suffix = ENHANCED
include_settings_in_suffix = False
preview_input = False
preview_settings = False
frame_to_preview = 777
```

# StreamLit
  ```streamlit run app.py```

# Demos


https://github.com/user-attachments/assets/9884f2f2-6de4-49c6-bb97-3c5a49886cd2




https://github.com/user-attachments/assets/984aede8-916f-45aa-a0cd-82f2918914bc




https://github.com/user-attachments/assets/50094318-f2cb-4cf6-ae67-67961da92af3


https://github.com/user-attachments/assets/186258eb-a6dd-4ef1-a07c-30e5c578d463

