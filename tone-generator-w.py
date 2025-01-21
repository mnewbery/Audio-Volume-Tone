import numpy as np # type: ignore
import sounddevice as sd  # type: ignore
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL  # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # type: ignore
import math

def generate_tone(frequency, duration, sample_rate=44100):
    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate sine wave tone
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone

def play_tone(tone, sample_rate=44100):
    sd.play(tone, sample_rate)
    sd.wait()  # Wait until the sound has finished playing

if __name__ == "__main__":
    frequency = 400  # Frequency in Hz (A4 note)
    duration = 2.0   # Duration in seconds
    tone = generate_tone(frequency, duration)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume 
    currentVolumeDb = volume.GetMasterVolumeLevel()
    volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
    play_tone(tone)    
    volume.SetMasterVolumeLevel(currentVolumeDb - 0, None)    
    play_tone(tone)
