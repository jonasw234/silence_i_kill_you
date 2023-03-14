#!/usr/bin/env python3
"""Remove silence from a video file.

Usage: silence_i_kill_you PATH [--db=<int>] [--duration=<int>] [--verbose]

Options:
    -l <int>, --db=<int>        Decibel level for silence [default: -30]
    -d <int>, --duration=<int>  Silence duration in seconds [default: 1]
    -v, --verbose               Verbose output

Original source: https://gist.github.com/antiboredom/8808d04c86ee13e5cf55b1347e043e20
"""
import logging
import os
import re
import subprocess
from typing import Tuple

from docopt import docopt
from moviepy.editor import VideoFileClip, concatenate_videoclips

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


def get_silences(filename: str, db: int, duration: int) -> str:
    """Get silences from video file by filtering with `ffmpeg`.

    Params
    ------
    filename : str
        The file name of the input file
    db : int
        Minimum decibel to detect as silence
    duration : int
        Minimum duration in seconds for silence

    Returns
    -------
    str
        Name of the output file with silence information
    """
    args = f'ffmpeg -nostats -i "{filename}" -af silencedetect=noise={db}dB:d={duration} -f null -'
    results = subprocess.getoutput(args)
    outname = f"{filename}.silences.txt"
    with open(outname, "w", encoding="utf8") as outfile:
        outfile.write(results)
    return outname


def parse_silences(filename: str) -> list[Tuple[float, float]]:
    """Parse silences by reading from a file and return them.

    Params
    ------
    filename : str
        The input file with silence information

    Returns
    -------
    list[Tuple[float, float]]
        List of silences as tuples of (start, end)
    """
    with open(filename, "r", encoding="utf8") as infile:
        lines = infile.readlines()

    out = []
    start = None
    end = None
    for line in lines:
        if "silencedetect" not in line:
            continue
        if start is None:
            results = re.search(r"silence_start: ([0-9.]+)", line)
            if results:
                start = float(results.group(1))
        else:
            results = re.search(r"silence_end: ([0-9.]+)", line)
            if results:
                end = float(results.group(1))
            logging.debug("Silence detected between %f and %f.", start, end)
            out.append((start, end))
            start = None
            end = None
    return out


def compose(videofile: str, silences: list[Tuple[float, float]]) -> str:
    """Compose a new video file based on the original file passed in as `videofile` with `silences`
    removed.

    Params
    ------
    videofile : str
        The path of the original video file
    silences : list[Tuple[float, float]]
        The list of silences in the video file

    Returns
    -------
    str
        The file name of the output file with silences removed
    """
    filename, file_extension = os.path.splitext(videofile)
    movie = VideoFileClip(videofile)
    clips = []
    previous_end = 0
    for start, end in silences:
        # keep non-silence between previous end and current start
        non_silence_start = previous_end
        non_silence_end = start
        if non_silence_start != non_silence_end:
            logging.debug(
                "Adding non-silent part from %f to %f to the list.",
                non_silence_start,
                non_silence_end,
            )
            non_silence_clip = movie.subclip(non_silence_start, non_silence_end)
            clips.append(non_silence_clip)

        previous_end = end

    # keep non-silence between last silence and end of video
    non_silence_start = previous_end
    non_silence_end = movie.duration
    if non_silence_start != non_silence_end:
        logging.debug(
            "Adding non-silent part from %f to %f to the list.",
            non_silence_start,
            non_silence_end,
        )
        non_silence_clip = movie.subclip(non_silence_start, non_silence_end)
        clips.append(non_silence_clip)

    outname = f"{filename}_silences_removed{file_extension}"
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(
        outname,
        codec="libx264",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        audio_codec="aac",
    )
    return outname


if __name__ == "__main__":
    args = docopt(__doc__)
    if args["--verbose"]:
        logging.getLogger().setLevel(logging.DEBUG)
    videofile = args["PATH"]

    logging.info("Detecting silence in %s ...", videofile)
    silence_file = get_silences(videofile, args["--db"], args["--duration"])
    logging.info("Silence detected, parsing file ...")
    silences = parse_silences(silence_file)
    logging.info("Removing silence from file and saving as new file.")
    compose(videofile, silences)
