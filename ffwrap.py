import sys

from io_handler import parse_args, print_command, print_metadata, check_inputs, check_outputs, print_result
from subprocess_handler import spawn_ffmpeg


if __name__ == '__main__':
    command, inputs, outputs = parse_args(sys.argv[1:])
    print_command(command)

    check_inputs(inputs)
    check_outputs(outputs, command)

    print_metadata(inputs)

    exit_code, duplicated_frames, dropped_frames = spawn_ffmpeg(command)

    print_result(exit_code, duplicated_frames, dropped_frames)
