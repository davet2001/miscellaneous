#!/bin/python3

# Helper script to prepare training data sets for piper voice model training.
# Usage:
# Collect a set of audio files (any ffmpeg readable format .e.g. mp3 etc),
# They must all have different names.
# Call the python script from the command line, specifying a file pattern as a command line parameter
# e.g.
#
# python3 prep_piper_training_set.py ~/Downloads/character1/*.mp3
#
# The script will then go through each file, transcribe the audio to a piper training compatible 
# transcript.csv file, and transcode all audio into 22050 Hz 16bit mono .wav, then
# save them as a zip.
#
# The two files can be shared via google drive to a link at:
# https://github.com/davet2001/piper/blob/master/notebooks/piper_multilingual_training_notebook.ipynb
# The python notebook can be run on google colab.
# Training for >2hours is recommended, and at least 5mins of audio seems to be necessary.
#
# Tips:
# Check the transcripts before submitting, to remove any errors. 
# Also remove any files that don't contain pure speech.


import glob
import sys
import os
import whisper
import subprocess
from pathlib import Path
import shutil

USAGE = f"{os.path.basename(__file__)} <file_pattern>"
TRANSCRIPT_FILE = "transcript.csv"
OUTPUT_DIR= "wavs/"
OUTPUT_ZIP="wavs"


def process_file(infile):
    #Transcribe the audio file using whisper
    print(f"processing {infile}")
    model = whisper.load_model("small")
    result = model.transcribe(infile)
    text = result["text"].strip()
    print(text)

    outfile = OUTPUT_DIR + Path(infile).stem + ".wav"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Now re-encode
    print("running ffmpeg...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",                   # overwrite if exists
            "-i", infile,           # input file 
            "-ar", "22050",         # audio sample rate
            "-acodec", "pcm_s16le", # codec pcm16bit
             "-ac", "1",            # 1 audio channel (mono)
            outfile
        ],
        check=True
    )

    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as transcript:
        transcript.write(f"{outfile}|{text}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Syntax error. Usage:\n")
        print(USAGE)
        exit(1)
    # Delete old file
    if os.path.exists(TRANSCRIPT_FILE):
        os.remove(TRANSCRIPT_FILE)

    files = sys.argv[1:]
    for file in files:
        process_file(file)

    shutil.make_archive(OUTPUT_ZIP, 'zip', ".", OUTPUT_DIR)
