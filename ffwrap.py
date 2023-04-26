import sys
from datetime import datetime
from src.colors import Col

from src.io_handler import parse_args, print_command, print_metadata, check_inputs, check_outputs, print_result
from src.misc import format_timedelta
from src.subprocess_handler import spawn_ffmpeg
from src.database import Database


if __name__ == '__main__':
    start_time = datetime.now()
    command, inputs, outputs, args_are_valid = parse_args(sys.argv[1:])
    if not args_are_valid:
        print(f'{Col.fail}Invalid arguments. Maybe you forgot an "-o"?{Col.endc}')
        exit(1)
    db_id = None
    with Database() as db:
        db_id = db.initialize_entry(
            command=' '.join(command),
            inputs=':::'.join(inputs),
            outputs=':::'.join(outputs),
            start_time=start_time.strftime('%Y-%m-%d %H:%M:%S')
        )
        if not db_id:
            print(f'{Col.fail}Could not initialize database entry{Col.endc}')
            exit(1)

    print_command(command)

    if not check_inputs(inputs):
        with Database() as db:
            db.update(
                id=db_id,
                exit_code=1,
                end_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                duplicated_frames=0,
                dropped_frames=0,
                total_time=int((datetime.now() - start_time).total_seconds()),
                message='INCOMPLETE'
            )
        exit(1)

    if not check_outputs(outputs, command):
        with Database() as db:
            db.update(
                id=db_id,
                exit_code=1,
                end_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                duplicated_frames=0,
                dropped_frames=0,
                total_time=int((datetime.now() - start_time).total_seconds()),
                message='INCOMPLETE'
            )
        exit(1)

    print_metadata(inputs)

    exit_code, duplicated_frames, dropped_frames = spawn_ffmpeg(command)

    end_time = datetime.now()
    print_result(exit_code, duplicated_frames,
                 dropped_frames, format_timedelta(end_time - start_time))

    if db_id:
        with Database() as db:
            db.update(
                id=db_id,
                total_time=int((end_time - start_time).total_seconds()),
                end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                exit_code=exit_code,
                duplicated_frames=duplicated_frames,
                dropped_frames=dropped_frames,
                message='SUCCESS' if exit_code == 0 else 'FAILED'
            )
