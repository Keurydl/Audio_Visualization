import os
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import wave
import time
from scipy.fft import fft
import librosa
import librosa.display
from tkinter import Tk, filedialog, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

class AudioVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Visualization Tool")
        self.root.geometry("1000x800")
        
        # Audio parameters
        self.CHUNK = 1024 * 4
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recording = False
        self.frames = []
        self.audio_data = None
        self.sample_rate = None
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Buttons
        ttk.Button(control_frame, text="Load Audio", command=self.load_audio).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Start Recording", command=self.start_recording).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Stop Recording", command=self.stop_recording).pack(side='left', padx=5)
        
        # Visualization type selection
        self.viz_type = ttk.Combobox(control_frame, 
                                   values=["Waveform", "Spectrum", "Spectrogram", "Mel Spectrogram"],
                                   state="readonly")
        self.viz_type.set("Waveform")
        self.viz_type.pack(side='left', padx=5)
        self.viz_type.bind('<<ComboboxSelected>>', self.update_visualization)
        
        # Matplotlib figure
        self.fig = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Default empty plot
        self.ax.set_title("Load an audio file or start recording")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
        self.canvas.draw()
    
    def load_audio(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.wav *.mp3 *.ogg"), ("All Files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            self.audio_data, self.sample_rate = librosa.load(file_path, sr=None, mono=True)
            self.update_visualization()
        except Exception as e:
            self.show_error(f"Error loading audio: {str(e)}")
    
    def start_recording(self):
        if self.recording:
            return
            
        self.recording = True
        self.frames = []
        
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.audio_callback
        )
        
        self.stream.start_stream()
        self.update_visualization()
    
    def stop_recording(self):
        if not self.recording:
            return
            
        self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        if self.frames:
            self.audio_data = np.frombuffer(b''.join(self.frames), dtype=np.int16)
            self.sample_rate = self.RATE
            self.update_visualization()
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)
    
    def update_visualization(self, event=None):
        if not hasattr(self, 'audio_data') or self.audio_data is None:
            return
            
        self.ax.clear()
        viz_type = self.viz_type.get()
        
        try:
            if viz_type == "Waveform":
                self.plot_waveform()
            elif viz_type == "Spectrum":
                self.plot_spectrum()
            elif viz_type == "Spectrogram":
                self.plot_spectrogram()
            elif viz_type == "Mel Spectrogram":
                self.plot_mel_spectrogram()
                
            self.canvas.draw()
        except Exception as e:
            self.show_error(f"Error in visualization: {str(e)}")
    
    def plot_waveform(self):
        time_axis = np.linspace(0, len(self.audio_data) / self.sample_rate, num=len(self.audio_data))
        self.ax.plot(time_axis, self.audio_data)
        self.ax.set_title("Audio Waveform")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Amplitude")
    
    def plot_spectrum(self):
        n = len(self.audio_data)
        yf = fft(self.audio_data)
        xf = np.linspace(0, self.sample_rate/2, n//2)
        self.ax.plot(xf, 2.0/n * np.abs(yf[:n//2]))
        self.ax.set_title("Frequency Spectrum")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("Magnitude")
    
    def plot_spectrogram(self):
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.audio_data)), ref=np.max)
        img = librosa.display.specshow(D, y_axis='log', x_axis='time', sr=self.sample_rate, ax=self.ax)
        self.fig.colorbar(img, ax=self.ax, format="%+2.0f dB")
        self.ax.set_title("Spectrogram")
    
    def plot_mel_spectrogram(self):
        S = librosa.feature.melspectrogram(y=self.audio_data, sr=self.sample_rate)
        S_dB = librosa.power_to_db(S, ref=np.max)
        img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=self.sample_rate, ax=self.ax)
        self.fig.colorbar(img, ax=self.ax, format='%+2.0f dB')
        self.ax.set_title('Mel-frequency spectrogram')
    
    def show_error(self, message):
        self.ax.clear()
        self.ax.text(0.5, 0.5, message, 
                    horizontalalignment='center',
                    verticalalignment='center',
                    transform=self.ax.transAxes,
                    color='red')
        self.canvas.draw()
    
    def on_closing(self):
        self.stop_recording()
        if self.p:
            self.p.terminate()
        self.root.destroy()

def main():
    root = Tk()
    app = AudioVisualizer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()