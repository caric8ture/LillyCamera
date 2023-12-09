import argparse
import time
import os
from datetime import datetime
from picamera2 import Picamera2

interval = 30   # Time in seconds between image captures
duration = 180  # Total time to run in seconds.  0 = continuous run
folder_prefix = ""

parser = argparse.ArgumentParser(description="Time-lapse camera program")
parser.add_argument(
    "-i",
    "--interval",
    type=int,
    default=interval,
    help=f"Time between captured images (in seconds)"
)
parser.add_argument(
    "-d",
    "--duration",
    type=int,
    default=duration,
    help=f"Total time to capture images"
)
parser.add_argument(
    "-f",
    "--folder",
    default=folder_prefix,
    help="camera specific name to add to folder path"
)

args = parser.parse_args()
if args.interval is not None:
    interval = args.interval

if args.duration is not None:
    duration = args.duration

if args.duration is not None:
    folder_prefix = f"{args.folder}-"

picam2 = Picamera2()
capture_config = picam2.create_still_configuration({'size': (1920, 1080)})
picam2.configure(capture_config)

start_time = time.time()
has_completed_duration = False


def duration_calculation():
    completed_duration = False
    if duration != 0:
        if time.time() - start_time > duration:
            completed_duration = True
    return completed_duration


while not has_completed_duration:
    ts = datetime.now()

    folder = f"tlapse/{folder_prefix}{ts.strftime('%Y-%m-%d')}/"
    os.system(f"mkdir -p {folder}")
    ts_string = ts.strftime('%Y-%m-%d-%H-%M-%S')
    picam2.start()
    picam2.capture_file(f"{folder}{ts_string}.jpg")
    picam2.stop()
    has_completed_duration = duration_calculation()
    time.sleep(interval)



