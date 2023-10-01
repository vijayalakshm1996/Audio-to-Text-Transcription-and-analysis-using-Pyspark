# project-team_13

### Final Code Files
- Final File Used for Speech to Text conversion : speech_to_text.py
- Final File Used for Query Processing : 532_project_data_preprocessing_query_preprocessing.ipynb

project-team_13 created by GitHub Classroom

### Install Required Packages
- `pip install SpeechRecognition`

- `pip install pydub`

- `python -m pip install pymongo==3.7.2`

- `pip install azure`

- `pip install pyspark`

### Functions for Speech to Text 
- `mp3_to_wav_Conversion(mp3_src, wav_dst)` to convert mp3 audio files to .wav format to be given to SpeechRecognition API.

- `split_files_with_timestamp(test_audio)` splits .wav files to 10 seconds chunks (granularity is of 10 seconds).

- `writeInFile_key_value(filename, key, value)` outputs the timestamp with transcribed data.

### Functions for Query Processing
- `import_data_from_blob_storage` to import files frm blob storage and convert to pandas dataframe.

- `preprocessing(dict_df)` to preprocess dataframe. Dictionary of dataframes imported from Azure Blob Storage is given as inputs.

- `write_to_db(df)` to write the dataframe to mongodb collection 

- `query_processing_course(course_number=None)` query the required dataframe based on course number

- `query_processing_date(data_spark,day=None,month_val=None,year_val=None)` query dataframe based on date. All parameters are optional

- `query_processing_text(final_output,txt)` query dataframe based on text

