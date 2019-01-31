import sys
import os
import subprocess


def play_sound(sound_path):
    if 'linux' in sys.platform:
        subprocess.call(['play', '-q', sound_path])
    elif 'win' in sys.platform:
        subprocess.call(['start', sound_path])
