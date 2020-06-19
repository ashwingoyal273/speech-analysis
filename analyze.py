import argparse, warnings
warnings.filterwarnings("ignore")
from speech_analysis import Process

parser = argparse.ArgumentParser(description="Process an audio file")
parser.add_argument('filename', type=str, help='Location of the audio file')
parser.add_argument('--noise', type=bool, default=False)
parser.add_argument('--sd', type=int, default=100, help='Silence duration')
parser.add_argument('--st', type=int, default=-16, help='Silence threshold')
args = parser.parse_args()

speech = Process(args.filename, args.noise, args.sd, args.st)
speech.recognize()
speech.silence_detection()
speech.words_per_minute()
speech.word_frequency()
