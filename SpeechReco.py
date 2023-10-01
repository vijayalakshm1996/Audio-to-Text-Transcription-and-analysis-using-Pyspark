# PLEASE READ THE COMMENTS and PROVIDE REVIEW COMMENTS IN THE CODE
# This file take mp3 file as an input and produces <key,value> pair of <timestamp,transcribed text> in a single file using Google's Speech recognition library.
#This pair can later be pre-processed for deleting the articles, prepositions, conjections etc.. and can be added to the DB
#The granularity is currently set as 10 seconds. we can reduce or increase it depending.


#Trial Number#1: with 532 recording on Oct12.(1:15 hrs) <-- the transcribed text does not match with the actual words due to an unique accent.
#Trial Number#2: with 661 recording by Brian Levine(20 mins) <-- the transcribed output is perfect.

#TBD::: what is the time granularity? which timestamp style do we use? Need american accent dataset, to get proper result.
#Next step of code addition::: 
#       Loop through multiple videos
#       Timestamp correction
#       add the results in the DB
#       eliminate unimportant words

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

#Round 1 - converting Oct12.mp3 to oct12.wav --> Currently doing only for a single lecture to understand Speechrecognition
mp3_src = "/Users/swathinatarajan/Documents/College_Admission/UMass/Courses/COMPSCI_532/Project/Project_Dataset/661_recordings/Lec1.mp3"
wav_dst = "/Users/swathinatarajan/Documents/College_Admission/UMass/Courses/COMPSCI_532/Project/Project_Dataset/661_recordings/Lec1.wav"
test_audio = mp3_to_wav_Conversion(mp3_src, wav_dst)

#split the huge audio file into smaller chunks of 1 sec each
chunks = split_files_with_timestamp(test_audio)
print(chunks)

#Export all of the individual chunks as wav files
for i, chunk in enumerate(chunks):
    chunk_name = "chunk{0}.wav".format(i)
    print("split#",i,"--",chunk_name)
    chunk.export("Trial2_661_Lec1/"+chunk_name, format="wav") 

    #Round 1 - working on a random chunk439.wav to check the transcription recognize_google() function.
    #Round 2 - Doing for all the chunks.
    chunk_audioname  = "Trial2_661_Lec1/"+chunk_name
    print(chunk_audioname)
    chunk_filename = "Trial2_661_Lec1/TranscriptOutput.txt"
    with sr.AudioFile(chunk_audioname) as source:
        audio_listened = r.record(source)
        try:        
            tsc_value = r.recognize_google(audio_listened)
            print(tsc_value)
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

       
        
               
