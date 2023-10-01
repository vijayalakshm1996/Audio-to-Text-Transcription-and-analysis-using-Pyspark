import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import subprocess
import time

def mp3_to_wav_Conversion(mp3_src, wav_dst):
    subprocess.call(['ffmpeg', '-i', mp3_src,wav_dst])
    #test audio of the dst file
    test_audio = AudioSegment.from_file(wav_dst , "wav") 
    return test_audio

def split_files_with_timestamp(test_audio):
    chunk_length_ms = 10000 
    chunks = make_chunks(test_audio, chunk_length_ms) 
    return chunks

def writeInFile_key_value(filename, key, value):
    with open(filename, "a") as f:
        f.write(str(key)+"th second:\t"+value+"\n")

#Speech recognition object declaration
r = sr.Recognizer()

mp3_src = "/content/drive/MyDrive/532_Systems_For_DS_Project/Transcription_experiments/532_dataset/"
mp3_folder = os.listdir(mp3_src)
wav_folder = "/content/drive/MyDrive/532_Systems_For_DS_Project/Transcription_experiments/wav_folder/"

for recording in mp3_folder:
    start_time = time.time()

    if "mp3" not in recording:
        continue

    file_name = recording.split(".")[0]
    print(file_name)
    mp3_file_path = mp3_src + recording
    wav_file_path = wav_folder + file_name + ".wav"
    test_audio = mp3_to_wav_Conversion(mp3_file_path, wav_file_path)
    chunks = split_files_with_timestamp(test_audio)
    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)

        chunk_folder = "/content/drive/MyDrive/532_Systems_For_DS_Project/Transcription_experiments/chunks/" + file_name +"/"
        
        if not os.path.exists(chunk_folder):
            os.makedirs(chunk_folder)
        
        chunk_location = chunk_folder + chunk_name
        chunk.export(chunk_location, format="wav") 

        #Round 1 - working on a random chunk439.wav to check the transcription recognize_google() function.
        #Round 2 - Doing for all the chunks.
        chunk_audioname  = chunk_location
        chunk_filename = "/content/drive/MyDrive/532_Systems_For_DS_Project/Transcription_experiments/output/" + file_name + ".txt";
        with sr.AudioFile(chunk_audioname) as source:
            audio_listened = r.record(source)
            try:        
                tsc_value = r.recognize_google(audio_listened)
                #Here is where the timestamp is added.
                #Now, the granularity is set as 10 seconds and adding in a different file
                #Round 2 - So the key value is 0 , 10 , 20, 30 seconds. 
                #Round 3 - make it as timestamp and try adding in single file
                tsc_key = i*10
                writeInFile_key_value(chunk_filename, tsc_key, tsc_value)
            except sr.UnknownValueError as err:
                    print("Empty", str(err))
            except sr.WaitTimeoutError as uErr:
                    print("WaitTimeOutError",str(uErr))
                    time.sleep(5)
                    continue
            except sr.RequestError as rErr:
                    time.sleep(5)
                    continue
    

    with open("/content/drive/MyDrive/532_Systems_For_DS_Project/Transcription_experiments/time/time.txt", "a") as f:
        f.write(file_name + " takes -> " + (str)(time.time() - start_time) + " seconds\n")
