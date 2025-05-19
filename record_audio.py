import pyaudio         # For accessing the microphone and capturing audio
import wave            # For saving the audio as a .wav file
import threading       # To run the recording in a background thread

class AudioRecorder:
  def __init__(self):
    # Flag to signal when to stop recording
    self.stop = False

    # Thread object to run the recording in the background
    self.thread = None

  def record(self, filename, fs=44100, chunk=1024):
    """
    Records audio from the default input device and saves it to a .wav file.

    Args:
      filename (str): The name of the file to save the recording to.
      fs (int): The sampling rate (default 44100 Hz).
      chunk (int): The number of audio frames per buffer (default 1024).
    """
    sample_format = pyaudio.paInt16  # 16-bit resolution
    channels = 2                     # Stereo input

    # Initialize PyAudio and open an input stream
    p = pyaudio.PyAudio()
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # List to store audio chunks

    # Continuously read audio chunks until stop flag is set
    while not self.stop:
      data = stream.read(chunk)
      frames.append(data)

    # Stop and close the stream and terminate PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save recorded frames to a .wav file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

  def start(self, filename):
    """
    Starts recording audio in a background thread.
    
    Args:
      filename (str): The name of the file to save the recording to.
    """
    self.stop = False
    self.thread = threading.Thread(target=self.record, args=(filename,))
    self.thread.start()

  def stop_recording(self):
    """
    Signals the recording to stop and waits for the background thread to finish.
    """
    self.stop = True
    if self.thread:
      self.thread.join()
