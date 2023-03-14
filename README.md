# silence_i_kill_you

Removes silence from video files

## Usage
```
Usage: silence_i_kill_you PATH [--db=<int>] [--duration=<int>] [--verbose]

Options:
    -l <int>, --db=<int>        Decibel level for silence [default: -30]
    -d <int>, --duration=<int>  Silence duration in seconds [default: 1]
    -v, --verbose               Verbose output
"""
```

## Installation
This needs [`ffmpeg`](https://ffmpeg.org/) in your PATH.

For the development version:
```
git clone https://github.com/jonasw234/silence_i_kill_you
cd silence_i_kill_you
python3 setup.py install
pip3 install -r dev-requirements.txt
```
For normal usage do the same but don’t include the last line or use [`pipx`](https://pypi.org/project/pipx/) and install with
```
pipx install git+https://github.com/jonasw234/silence_i_kill_you
```

## Credits
Original source: https://gist.github.com/antiboredom/8808d04c86ee13e5cf55b1347e043e20
