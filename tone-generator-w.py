import numpy as np # type: ignore
import sounddevice as sd  # type: ignore
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL  # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # type: ignore
import math
import matplotlib.pyplot as plt
from scipy import signal

def generate_tone(frequency, duration, sample_rate=44100):
    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate sine wave tone
    return 0.5 * np.sin(2 * np.pi * frequency * t)    

def generate_triangle_tone(frequency, duration, sample_rate=44100):
    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate triangle wave tone
    return signal.sawtooth(2 * np.pi * frequency * t, 0.5)

def generate_square_tone(frequency, duration, sample_rate=44100):
    # Generate time values
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Generate triangle wave tone
    return signal.square(2 * np.pi * frequency * t, 0.5)

def play_tone(tone, sample_rate=44100):
    show_tone(tone, sample_rate)
    sd.play(tone, sample_rate)
    sd.wait()  # Wait until the sound has finished playing
    
def show_tone(tone, sample_rate):
    fig = plt.figure()
    fig.subplots_adjust(top=0.8)
    ax1 = fig.add_subplot(211)
    ax1.set_ylabel('Voltage [V]')
    ax1.set_xlabel('Milliseconds [mS]')
    ax1.set_title('Tone wave')
    # Plotting frequency over 100 ms means there are steps every 100/sample_rate 
    array_1 = []
    divisor = sample_rate/100 # sample the first 100ms
    for number in tone:
        array_1.append(number)
        if len(array_1) >= divisor:
            break
    
    t = np.arange(0.0, 100, 100/len(array_1)) # scale to 100ms
    line, = ax1.plot(t, array_1, color='blue', lw=2)
    plt.show()
    
def do_main():
    frequency = 400  # Frequency in Hz (A4 note)
    duration = 2.0   # Duration in seconds
    tone_square = generate_square_tone(frequency, duration)
    tone_triangle = generate_triangle_tone(frequency, duration)
    tone = generate_tone(frequency, duration)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get the current master volume level
    current_volume = volume.GetMasterVolumeLevelScalar()
    print(f"Current master volume level: {current_volume * 100:.2f}%")
    # Get current volume in Db
    currentVolumeDb = volume.GetMasterVolumeLevel()
    print(f"Current master volume level in dB: {currentVolumeDb}")    
    volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
    play_tone(tone_square)
    play_tone(tone_triangle)
    play_tone(tone)    
    volume.SetMasterVolumeLevel(currentVolumeDb - 0, None)    
    play_tone(tone)
    # Return to the value set prior to the code running
    volume.SetMasterVolumeLevel(currentVolumeDb, None)    

if __name__ == "__main__":
    do_main()
    exit()
