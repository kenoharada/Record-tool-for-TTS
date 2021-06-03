import pyaudio
import wave
import os
import glob
import time


DEVICE_INDEX = 3
CHUNK = 1024
FORMAT = pyaudio.paInt16 # 16bit
CHANNELS = 1             # monaural
RATE = 48000             # sampling frequency [Hz]


def get_wav_duration(wav_path):
    wf = wave.open(wav_path, 'rb')
    # ch = wf.getnchannels()
    # width = wf.getsampwidth()
    fr = wf.getframerate()
    fn = wf.getnframes()
    total_time = 1.0 * fn / fr
    wf.close()
    return total_time


def play(wav_path):
    wf = wave.open(wav_path, 'rb')
    play = pyaudio.PyAudio()

    # open stream (2)
    play_stream = play.open(format=play.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play. stream (3)
    while len(data) > 0:
        play_stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    play_stream.stop_stream()
    play_stream.close()

    # close PyAudio (5)
    play.terminate()
    wf.close()


def record(output_path, limit_time):
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = DEVICE_INDEX,
                frames_per_buffer=CHUNK)
    print("RECORD START")
    print("ctrl-C : STOP RECORDING")

    # RECORDING ###############
    # Stop with Ctrl-C
    frames = []
    for i in range(0, int(RATE / CHUNK * limit_time)):
        try:
            # Record
            data = stream.read(CHUNK)
            frames.append(data)

        except KeyboardInterrupt:
            # Ctrl - c  
            break
    print("End Recodring")
    # END # RECORDING ###############

    # CLOSE
    stream.stop_stream()
    stream.close()
    pa.terminate()
    wf = wave.open(output_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def ask_retry():
    print("Retry? push r")
    print("Go to Next? push n")
    while True:
        ans = input()
        if ans == 'r':
            retry = True
            break
        elif ans == "n":
            retry = False
            break
        else:
            print("push r or n")
            continue
    return retry


if __name__ == '__main__':
    SAMPLE_DIR_PATH = 'jsut_ver1.1/basic5000'
    OUTPUT_PATH = 'original_data/basic5000'
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
        os.makedirs(f'{OUTPUT_PATH}/wav')
    # transcript_utf8.txt
    # BASIC5000_0001:水をマレーシアから買わなくてはならないのです。
    # BASIC5000_0002:木曜日、停戦会談は、何の進展もないまま終了しました。
    annotations = set(open(f'{SAMPLE_DIR_PATH}/transcript_utf8.txt').read().split('\n')[:-1])
    recorded_annotations = set(open(f'{OUTPUT_PATH}/transcript_utf8.txt').read().split('\n')[:-1]) if os.path.exists(f'{OUTPUT_PATH}/transcript_utf8.txt') else set()
    annotations = annotations - recorded_annotations
    annotations = sorted(list(annotations))
    for annotation in annotations:
        retry = True
        while retry:
            wav_file_name = annotation.split(':')[0]
            subtitles = annotation.split(':')[1]
            print(subtitles)
            limit_time = get_wav_duration(f'{SAMPLE_DIR_PATH}/wav/{wav_file_name}.wav') + 0.5
            play(f'{SAMPLE_DIR_PATH}/wav/{wav_file_name}.wav')
            record(f'{OUTPUT_PATH}/wav/{wav_file_name}.wav', limit_time)
            print('your voice')
            play(f'{OUTPUT_PATH}/wav/{wav_file_name}.wav')
            retry = ask_retry()
        with open(f'{OUTPUT_PATH}/transcript_utf8.txt', 'a') as f:
            f.write(f'{wav_file_name}:{subtitles}\n')