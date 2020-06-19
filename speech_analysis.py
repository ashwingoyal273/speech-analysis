import speech_recognition as sr
from pydub import AudioSegment, silence
from collections import defaultdict
import os


class Process:
    """
    Speech processing class
    """

    def __init__(self, audio_file_name, noise=False, silence_duration=100, silence_threshold=-16):
        """
        :param audio_file_name: (String) location of the audio file
        :param noise: (Bool) if the file contains noises apart from speech
        :param silence_duration: (int) minimum silence duration in ms
        :param silence_threshold: (int) maximum silence threshold in db
        """
        if audio_file_name is None:
            raise Exception("Audio file name not provided")
        self.supported = {"wav"}
        self.audio_file = audio_file_name
        self.silence_duration = silence_duration
        self.silence_threshold = silence_threshold
        self.audio_length = len(AudioSegment.from_wav(self.audio_file))
        self.words = None
        self.wpm = None
        self.wf = defaultdict(int)
        self.noise = noise
        self.output_file = 'output/{}_output.txt'.format(self.audio_file.replace('.', '_'))
        if not os.path.exists('output'):
            os.makedirs('output')
        with open(self.output_file, 'w') as f:
            f.write("For audio file: {}\n".format(self.audio_file))
        audio_file_name = audio_file_name.split('.')
        if audio_file_name[-1] not in self.supported:
            raise Exception("Audio file not supported")

    def recognize(self):
        """
        Uses the Speech Recognition library to recognize words using Google Translate
        :return: void
        """
        audio_source = sr.AudioFile(self.audio_file)
        r = sr.Recognizer()
        with audio_source as source:
            if self.noise:
                r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.record(source)
        try:
            self.words = r.recognize_google(audio)
        except Exception as e:
            with open(self.output_file, 'a+') as f:
                f.write("\tNo words or No internet connection\n")
            return

        with open(self.output_file, 'a+') as f:
            f.write("\nTranscript:\n")
            f.write("{}\n".format(self.words))

        self.words = self.words.split(' ') if self.words else []

    def silence_detection(self):
        """
        Detects number of silences which are below a certain threshold and last for atleast a certain duration
        """
        audio = AudioSegment.from_wav(self.audio_file)
        silent = silence.detect_silence(audio, min_silence_len=self.silence_duration,
                                        silence_thresh=self.silence_threshold)
        with open(self.output_file, 'a+') as f:
            f.write("\nSilence Detection:\n")
            f.write("\tThe number of silences of atleast {}ms duration and threshold of {}db is : {}\n".format(
                self.silence_duration, self.silence_threshold, len(silent)))

    def words_per_minute(self):
        """
        Detects the number of words spoken per minute using google translate
        """
        with open(self.output_file, 'a+') as f:
            f.write("\nWords per minute:\n")

        self.wpm = len(self.words) / (self.audio_length / 60000)
        with open(self.output_file, 'a+') as f:
            f.write("\twpm: {}\n".format(self.wpm))

    def word_frequency(self):
        """
         Detects the frequency of each word spoken using Google translate
        """
        with open(self.output_file, 'a+') as f:
            f.write("\nWord frequency:\n")
        for word in self.words:
            self.wf[word] += 1
        with open(self.output_file, 'a+') as f:
            for w in self.wf:
                f.write("{} : {}\n".format(w, self.wf[w]))
