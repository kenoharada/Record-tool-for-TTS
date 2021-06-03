# Record-tool-for-TTS
GUI tool for recording audio data for training your Text To Speech model
## Prerequisites
### Install Pyaudio
```
$ brew install portaudio 
$ pip install pyaudio
```
## Prepare corpos data
```
$ wget http://ss-takashi.sakura.ne.jp/corpus/jsut_ver1.1.zip
$ unzip jsut_ver1.1.zip
$ rm jsut_ver1.1.zip
```

## Reference
- Pyaudio documentation: https://people.csail.mit.edu/hubert/pyaudio/docs/
- Pyaudio recording sample https://qiita.com/beeesssaaa/items/68342472694a3f74d86e