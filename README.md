# Audio Visualization Tool

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A powerful and interactive audio visualization tool built with Python that allows you to visualize audio files and live recordings in multiple ways.

## Features

- 🎧 Load and visualize audio files (WAV, MP3, OGG)
- 🎤 Record audio directly from your microphone
- 📊 Multiple visualization types:
  - Waveform
  - Frequency Spectrum (FFT)
  - Spectrogram
  - Mel Spectrogram
- 🖥️ User-friendly GUI built with Tkinter
- 🎨 Interactive plots with Matplotlib

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/audio-visualization.git
   cd audio-visualization-tool
   ```

2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install them manually:
   ```bash
   pip install numpy matplotlib pyaudio librosa scipy
   ```

## Usage

1. Run the application:
   ```bash
   python Audio.py
   ```

2. **Load an audio file**:
   - Click "Load Audio"
   - Select an audio file (WAV, MP3, or OGG)

3. **Or record audio**:
   - Click "Start Recording" to begin recording from your microphone
   - Click "Stop Recording" when finished

4. **Switch between visualizations**:
   - Use the dropdown menu to select different visualization types

## Visualization Types

- **Waveform**: Shows the amplitude of the audio signal over time
- **Spectrum**: Displays the frequency content using FFT
- **Spectrogram**: Visualizes how the frequency content changes over time
- **Mel Spectrogram**: Shows frequency content on the mel scale, which better represents human hearing

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- PyAudio
- Librosa
- SciPy

## Troubleshooting

- **Microphone not working**:
  - Ensure your microphone is properly connected
  - Check if other applications are using the microphone
  - On Linux, you might need to install `portaudio19-dev`:
    ```bash
    sudo apt-get install portaudio19-dev
    ```

- **Dependency installation issues**:
  - On Windows, you might need to install Microsoft C++ Build Tools
  - For PyAudio, you can try using a pre-built wheel:
    ```bash
    pip install pipwin
    pipwin install pyaudio
    ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## View:

![image](https://github.com/user-attachments/assets/be9a12f6-7444-4ad7-ae08-c65c88954b8d)

