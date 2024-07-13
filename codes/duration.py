from pydub import AudioSegment
import os

def get_flac_duration(flac_path):
    """ Returns the duration of a FLAC file in milliseconds, converted to seconds. """
    audio = AudioSegment.from_file(flac_path)
    return audio.duration_seconds

def list_flac_files(directory, output_file):
    """ Recursively lists all FLAC files in a directory, their durations, and writes them to a file. """
    total_duration = 0
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".flac"):
                    filepath = os.path.join(root, file)
                    duration = get_flac_duration(filepath)
                    f.write(f"{filepath}: {duration:.2f} seconds\n")
                    total_duration += duration
        f.write(f"Total duration: {total_duration:.2f} seconds")

# Specify the directory containing FLAC files and the output file
directory = '/mundus/data_mundus/slm/librilight-large'
# directory = '/mundus/abadawi696/slibrilight/syn-librilight-large-audio'
output_file = '/mundus/abadawi696/slibrilight/slibrilight-large/duration-large-mundus.txt'
list_flac_files(directory, output_file)
