import numpy as np
from scipy.io import wavfile
import os


def generate_slice_sound():
    # Create a slice sound (high frequency sweep)
    duration = 0.2
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate a frequency sweep from 2000Hz to 4000Hz
    freq_sweep = np.linspace(2000, 4000, len(t))
    signal = 0.5 * np.sin(2 * np.pi * freq_sweep * t)

    # Add a quick fade out
    fade_out = np.linspace(1, 0, len(t))
    signal *= fade_out

    # Convert to 16-bit PCM
    signal = (signal * 32767).astype(np.int16)

    # Save the sound
    os.makedirs("sounds", exist_ok=True)
    wavfile.write("sounds/slice.wav", sample_rate, signal)


def generate_bomb_sound():
    # Create a bomb sound (low frequency explosion)
    duration = 0.5
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Generate explosion sound with multiple frequencies
    signal = np.zeros_like(t)
    for freq in [50, 100, 200]:
        signal += 0.3 * np.sin(2 * np.pi * freq * t)

    # Add noise
    noise = np.random.normal(0, 0.1, len(t))
    signal += noise

    # Add exponential decay
    decay = np.exp(-5 * t)
    signal *= decay

    # Convert to 16-bit PCM
    signal = (signal * 32767).astype(np.int16)

    # Save the sound
    os.makedirs("sounds", exist_ok=True)
    wavfile.write("sounds/bomb.wav", sample_rate, signal)


def generate_background_music():
    # Create a simple background loop
    duration = 4.0  # 4 seconds loop
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # Create a simple melody
    melody = np.zeros_like(t)
    notes = [261.63, 293.66, 329.63, 349.23]  # C4, D4, E4, F4
    for i, note in enumerate(notes):
        start = i * duration / len(notes)
        end = (i + 1) * duration / len(notes)
        mask = (t >= start) & (t < end)
        melody[mask] = 0.2 * np.sin(2 * np.pi * note * (t[mask] - start))

    # Add a simple bass line
    bass = 0.1 * np.sin(2 * np.pi * 65.41 * t)  # C2

    # Combine and add fade in/out
    signal = melody + bass
    fade = np.ones_like(t)
    fade[:1000] = np.linspace(0, 1, 1000)
    fade[-1000:] = np.linspace(1, 0, 1000)
    signal *= fade

    # Convert to 16-bit PCM
    signal = (signal * 32767).astype(np.int16)

    # Save the sound
    os.makedirs("sounds", exist_ok=True)
    wavfile.write("sounds/background.wav", sample_rate, signal)


if __name__ == "__main__":
    generate_slice_sound()
    generate_bomb_sound()
    generate_background_music()
    print("Sound effects generated successfully!")
