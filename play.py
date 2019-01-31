import sys
import os
import subprocess

import pydub
import soundcard as sc
from pydub import effects


def play_sound1(sound_path):
    if 'linux' in sys.platform:
        subprocess.call(['play', '-q', sound_path])
    elif 'win' in sys.platform:
        subprocess.call(['start', sound_path])


def play_sound(sound_path, samplerate=16000):
    sound = pydub.AudioSegment.from_file(sound_path, 'wav')
    sound = sound.set_frame_rate(samplerate)
    sound = sound.set_channels(1)
    sound = sound.set_sample_width(2)
    sound = sound.remove_dc_offset()
    sound = effects.normalize(sound)
    signal = [i/65536 for i in sound.get_array_of_samples()]

    ds = sc.default_speaker()
    ds.play(signal, samplerate)



