import os

from .colors import Col
from .custom_types import Command, Inputs, Outputs, ExitCode, DuplicatedFrames, DroppedFrames, CommandID
from .subprocess_handler import get_metadata


def parse_args(args: list[str]) -> tuple[Command, Inputs, Outputs, bool, CommandID]:
    command = ['ffmpeg', '-v', 'warning', '-stats']
    inputs = []
    outputs = []
    args_are_valid = True
    custom_id = ''

    for idx, arg in enumerate(args):
        if arg == '-i':
            inputs.append(args[idx + 1])
            command.append(arg)
        elif arg == '-o':
            outputs.append(args[idx + 1])
        elif arg == '-ö':
            custom_id = args[idx + 1].lower()
        elif not args[idx - 1] == '-ö':
            command.append(arg)

    if len(outputs) > 0 and len(command) > command.index(outputs[-1]) + 1:
        if (
            len(command) == command.index(outputs[-1]) + 2 and
            command[-1] in ['-y', '-n']
        ):
            pass
        else:
            args_are_valid = False

    return command, inputs, outputs, args_are_valid, custom_id


def print_metadata(inputs: Inputs) -> None:
    for idx, i in enumerate(inputs):
        mi = get_metadata(i)
        if mi and mi['media']:
            mi_output = mi['media']
            print(
                f'\n{"----- - " * 10}\nInput #{idx} - "{Col.blue}{i}{Col.endc}":')
            if 'track' in mi_output:
                for track in mi_output['track']:
                    if track['@type'] == 'General':
                        format = f"{track['Format']}" if 'Format' in track else None
                        size = f"{track['FileSize_String']}" if 'FileSize_String' in track else None
                        duration = f"{track['Duration_String4']}" if 'Duration_String4' in track else None
                        bitdepth = f"{track['OverallBitRate_String']}" if 'OverallBitRate_String' in track else None

                        if (format or size or duration or bitdepth):
                            if '@typeorder' in track.keys():
                                print(
                                    f'  {Col.yellow}General{Col.endc} #{track["@typeorder"]}:', end='')
                            else:
                                print(
                                    f'  {Col.yellow}General{Col.endc}:', end='')
                            if format:
                                print(f'  format: {format}', end='')
                            if size:
                                print(f'  size: {size}', end='')
                            if duration:
                                print(f'  duration: {duration}', end='')
                            if bitdepth:
                                print(f'  bitrate: {bitdepth}', end='')
                            print()

                    elif track['@type'] == 'Video':
                        codec = f"{track['Format']}" if 'Format' in track else None
                        width = f"{track['Width']}" if 'Width' in track else None
                        height = f"{track['Height']}" if 'Height' in track else None
                        framerate = f"{track['FrameRate']}" if 'FrameRate' in track else None
                        SAR = f"{track['PixelAspectRatio']}" if 'PixelAspectRatio' in track else None
                        DAR = f"{track['DisplayAspectRatio']}" if 'DisplayAspectRatio' in track else None
                        scan = f"{track['ScanType']}" if 'ScanType' in track else None

                        if (codec or width or height or framerate or SAR or scan):
                            if '@typeorder' in track.keys():
                                print(
                                    f'  {Col.header}Video{Col.endc} #{track["@typeorder"]}:', end='')
                            else:
                                print(
                                    f'  {Col.header}Video{Col.endc}  :', end='')
                            if codec:
                                print(f'  codec: {codec}', end='')
                            if width and height:
                                print(
                                    f'  resolution: {width}x{height}', end='')
                            if SAR:
                                print(f'  SAR: {SAR}', end='')
                            if DAR:
                                print(f'  DAR: {DAR}', end='')
                            if framerate:
                                print(f'  framerate: {framerate}', end='')
                            if scan:
                                print(f'  scantype: {scan}', end='')
                            print()

                    elif track['@type'] == 'Audio':
                        codec = f"{track['Format']}" if 'Format' in track else None
                        channels = f"{track['Channels']}" if 'Channels' in track else None
                        samplerate = f"{track['SamplingRate_String']}" if 'SamplingRate_String' in track else None
                        bitdepth = f"{track['BitDepth_String']}" if 'BitDepth_String' in track else None

                        if (codec or channels or samplerate or bitdepth):
                            if '@typeorder' in track.keys():
                                print(
                                    f'  {Col.cyan}Audio{Col.endc} #{track["@typeorder"]}:', end='')
                            else:
                                print(
                                    f'  {Col.cyan}Audio{Col.endc}  :', end='')
                            if codec:
                                print(f'  codec: {codec}', end='')
                            if channels:
                                print(f'  channels: {channels}', end='')
                            if samplerate:
                                print(f'  samplerate: {samplerate}', end='')
                            if bitdepth:
                                print(f'  bitdepth: {bitdepth}', end='')
                            print()

                    elif track['@type'] == 'Image':
                        codec = f"{track['Format']}" if 'Format' in track else None
                        width = f"{track['Width']}" if 'Width' in track else None
                        height = f"{track['Height']}" if 'Height' in track else None
                        bitdepth = f"{track['BitDepth_String']}" if 'BitDepth_String' in track else None

                        if (codec or width or height):
                            if '@typeorder' in track.keys():
                                print(
                                    f'  {Col.header}Image{Col.endc} #{track["@typeorder"]}:', end='')
                            else:
                                print(
                                    f'  {Col.header}Image{Col.endc}:', end='')
                            if codec:
                                print(f'  codec: {codec}', end='')
                            if width and height:
                                print(
                                    f'  resolution: {width}x{height}', end='')
                            if bitdepth:
                                print(f'  bitdepth: {bitdepth}', end='')
                            print()

            else:
                print(f'{Col.warn}No tracks found{Col.endc}')
        else:
            print(
                f'\n{"----- - " * 10}\nInput #{idx} - "{Col.blue}{i}{Col.endc}":')
            print(f'{Col.warn}  No metadata found{Col.endc}')


def check_inputs(inputs: Inputs) -> bool:
    if not inputs:
        print(f'{Col.fail}No input specified. Exiting{Col.endc}')
        return False

    return True


def check_outputs(outputs: Outputs, command: Command) -> bool:
    if not outputs:
        print(f'{Col.fail}No output specified. Exiting{Col.endc}')
        return False

    existing_outputs = [
        o for o in outputs if os.path.exists(o)]
    if existing_outputs and not '-y' in command:
        overwrite = input(
            'Overwrite existing output(s)? [y/N] ')
        if overwrite.lower() != 'y':
            print(f'{Col.fail}Not overwriting. Exiting{Col.endc}')
            return False
        else:
            command += ['-y']
    elif existing_outputs and '-y' in command:
        print(
            f'{Col.bold}Option "-y" detected. Overwriting existing output(s){Col.endc}')
    elif existing_outputs and '-n' in command:
        print(
            f'{Col.bold}Option "-n" detected. Not overwriting existing output(s){Col.endc}')
        return False

    for o in outputs:
        dirname = os.path.dirname(o)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    return True


def print_command(command: Command) -> None:
    print(
        f'Spawning:\n  "{Col.green}{Col.underline}{" ".join(command)}{Col.endc}"\n')


def print_result(exit_code: ExitCode, duplicated_frames: DuplicatedFrames, dropped_frames: DroppedFrames, elapsed_time: str) -> None:
    print(
        f'\n{"----- - " * 10}\nFinished after: {Col.bold}{elapsed_time}{Col.endc}')
    col = Col.blue if exit_code == 0 else Col.fail
    print(
        f'{col}FFmpeg exited with code: {Col.bold}{exit_code}{Col.endc}')
    if duplicated_frames or dropped_frames:
        print(f'{Col.warn}Warning:{Col.endc}')
        if duplicated_frames:
            print(
                f'{Col.fail}  duplicated frames: {Col.bold}{duplicated_frames}{Col.endc}')
        if dropped_frames:
            print(
                f'{Col.fail}  dropped frames: {Col.bold}{dropped_frames}{Col.endc}')
