# speech-analysis

## Description
Speech Analysis program meant for the position of ICT AI Student programmer.
* Takes input as an audio file
* Outputs the number of silences, words per minute and the word frequency

## Requirements
* File must be .wav format
* Should have working internet connection

## Library Dependencies
* SpeechRecognition, please refer https://pypi.org/project/SpeechRecognition/ for documentation
* pydub, please refer https://github.com/jiaaro/pydub for documentation and installation guide

## Instructions:
  - run analyze.py
  - The following args need to be passed to analyze.py:
    * :param filename: (String) location of the audio file
    * :param --noise(default = False): (Bool) if the file contains noises apart from speech
    * :param --sd(default = 100): (int) minimum silence duration in ms
    * :param --st(default = -16): (int) maximum silence threshold in db
  - The output text file will be saved in the output directory in the following format:
    * ```'output/{}_output.txt'.format(self.audio_file.replace('.', '_')```
    * example : harvard.wav will be saved as harvard_wav_output.txt in output directory
## Sample:
      ```python analyze.py 'jackhammer.wav' --noise True```
## Code explaination:
  - The Process class uses pydub library to detect the number of silences, the silences are categorised with a minimum duration in ms and a maximum threshold in db.
  - It uses SpeechRecognition library to use google translate for recognising speech, this requires an active internet connection.
  - Also if the audio contains noise other than speech, we can set ```noise = True```, so that the first 0.5 seconds will be used to adjust the audio file for ambient noise.
  - If no Internet connection is available or no words are recognised, then the output file will mention that.
  

