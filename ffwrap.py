import subprocess
import os
from typing import IO

def read_stderr(stderr: IO[bytes]):
    return stderr.read(1).decode('utf-8')

env = os.environ.copy()

command = 'ffmpeg -v warning -stats -f lavfi -r 24 -i mandelbrot -t 10 -y -r 18 delme.mp4'

ffmpeg_process = subprocess.Popen(
    command.split(' '), stderr=subprocess.PIPE, env=env)

if ffmpeg_process.stderr:
    stde = ffmpeg_process.stderr
    dup = 0
    drop = 0
    line = ''
    for char in iter(lambda: read_stderr(stde), ''):
        line += char
        if char in ['\n', '\r']:
            if 'dup' in line:
                dup = int(line.split('dup=')[-1].split(' ')[0])

            if 'drop' in line:
                drop = int(line.split('drop=')[-1].split(' ')[0])

            print(line, end='')
            line = ''
    
    print(f'--- ---\nDropped frames: {drop}\nDuplicated frames: {dup}')
