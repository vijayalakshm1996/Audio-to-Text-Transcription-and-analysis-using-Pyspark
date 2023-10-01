'''
author: abhilasha_lodha
'''

import torch
import os
import librosa
import numpy as np
import soundfile as sf
from scipy.io import wavfile
from IPython.display import Audio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def speech2TextTransformer(folder_path):
	for files in os.listdir(folder_path):
		file_name = os.path.join(folder_path,files)
		data = wavfile.read(file_name)
		framerate = data[0]
		sounddata = data[1]
		time = np.arange(0,len(sounddata))/framerate
		input_audio, _ = librosa.load(file_name, sr=16000)
		input_values = tokenizer(input_audio, return_tensors="pt").input_values
		logits = model(input_values).logits
		predicted_ids = torch.argmax(logits, dim=-1)
		transcription = tokenizer.batch_decode(predicted_ids)[0]
		print(transcription)


folder_path = "/abhilasha_lodha/Documents/Systems_Project/output/661_output"
speech2TextTransformer(folder_path)

