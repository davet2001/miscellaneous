#!/bin/python
#
# Helper script to transcribe podcast files.
#
# Dave T 2024-10-15
# Takes a directory of audio files, and creates one big text file of the transcripts,
# broken into sections for each episode.

# The files need to be alphabetically in the order that you want them to 
# appear in the text file, so I recommend using an iso date prefix or similar.
#
# The main purpose is to have a rapidly searchable text file of a lot of audio data.

import sys
from faster_whisper import WhisperModel
from faster_whisper.transcribe import BatchedInferencePipeline
from pathlib import Path
import datetime
TRANSCRIPT_FILE = "podcast_transcript.txt"

USAGE = "transcribe_podcasts.py <file1.mp3> [file2.mp3 ...]"

def process_file(file):
    model = WhisperModel("small", device="cpu", compute_type="int8")
    batched_model = BatchedInferencePipeline(model=model)
    segments, info = batched_model.transcribe(file, batch_size=16)



    with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as transcript:
        transcript.write(f"{Path(file).stem}:\n")
        for segment in segments:
            start = str(datetime.timedelta(seconds=int(segment.start)))
            end = str(datetime.timedelta(seconds=int(segment.end)))
            text = segment.text
            print(f"[{start} -> {end}] {text}")
            transcript.write(f"[{start} -> {end}] {text}\n")
        transcript.write("\n===============================================================\n\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Syntax error. Usage:\n")
        print(USAGE)
        exit(1)

    files = sys.argv[1:]
    files.sort()
    for file in files:
        process_file(file)
