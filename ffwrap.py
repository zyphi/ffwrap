import sys
from datetime import datetime

from src.io_handler import parse_args, print_command, print_metadata, check_inputs, check_outputs, print_result
from src.misc import format_timedelta
from src.subprocess_handler import spawn_ffmpeg
from src.database import Database


if __name__ == '__main__':
    start_time = datetime.now()
    command, inputs, outputs = parse_args(sys.argv[1:])
    db_id = None
    with Database() as db:
        db_id = db.init_before_render(
            command=' '.join(command),
            inputs=':::'.join(inputs),
            outputs=':::'.join(outputs),
            start_time=start_time.strftime('%Y-%m-%d %H:%M:%S')
        )
    print_command(command)

    check_inputs(inputs)
    check_outputs(outputs, command)

    print_metadata(inputs)

    exit_code, duplicated_frames, dropped_frames = spawn_ffmpeg(command)

    end_time = datetime.now()
    print_result(exit_code, duplicated_frames,
                 dropped_frames, format_timedelta(end_time - start_time))

    if db_id:
        with Database() as db:
            db.update_after_render(
                id=db_id,
                total_time=int((end_time - start_time).total_seconds()),
                end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                exit_code=exit_code,
                duplicated_frames=duplicated_frames,
                dropped_frames=dropped_frames
            )
