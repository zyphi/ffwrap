import subprocess
import json
import os

from .colors import Col
from .custom_types import ExitCode, DuplicatedFrames, DroppedFrames


def get_metadata(i: str) -> dict:
    if i.endswith('.dpx'):
        parent = os.path.dirname(i) if os.path.dirname(i) else '.'
        first_frame = [f for f in os.listdir(parent) if f.endswith('.dpx')][0]
        mi_out_bytes = subprocess.check_output(
            ['mediainfo', '--Full', '--File_TestContinuousFileNames=0', '--Output=JSON', os.path.join(parent, first_frame)]).decode('utf-8')
    else:
        mi_out_bytes = subprocess.check_output(
            ['mediainfo', '--Full', '--Output=JSON', i]).decode('utf-8')
    return json.loads(mi_out_bytes)


def spawn_ffmpeg(command: list[str]) -> tuple[ExitCode, DuplicatedFrames, DroppedFrames]:
    print(f'\n{"----- - " * 10}\nFFmpeg output:\n')
    duplicated_frames = 0
    dropped_frames = 0

    ffmpeg_process = subprocess.Popen(
        command, stderr=subprocess.PIPE)

    if ffmpeg_process.stderr:
        stde = ffmpeg_process.stderr
        line = ''
        for char in iter(lambda: stde.read(1).decode('utf-8'), ''):
            line += char
            if char in ['\n', '\r']:
                if 'dup' in line:
                    duplicated_frames = int(
                        line.split('dup=')[-1].split(' ')[0])

                if 'drop' in line:
                    dropped_frames = int(line.split('drop=')[-1].split(' ')[0])

                col = Col.fail
                if line.startswith('frame=') or line.startswith('size=') or line.startswith('time=') or line.startswith('bitrate='):
                    col = Col.green
                elif line.startswith('['):
                    col = Col.blue
                print(f'{col}{line}{Col.endc}', end='')
                line = ''

    return ffmpeg_process.wait(), duplicated_frames, dropped_frames
