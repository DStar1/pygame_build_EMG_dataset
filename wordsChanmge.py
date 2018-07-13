import pandas as pd
import sys, os, subprocess
from datetime import datetime
from time import time

VERBOSITY = 100

def read_inputs(file):
    outputs = pd.read_csv(file, sep=',')
    # outputs.drop(outputs.index[0], inplace=True)
    # outputs = outputs.reset_index(drop=True)
    return outputs

def first_signal(df):
    return df.iloc[0]["timeStamp"]

def nearest_1000(n):
    return round(n / 1000) * 1000

def make_start_end_df(df):
    prevWord = None
    startEnd = pd.DataFrame()
    prev = 0
    for i, row in df.iterrows():
        word = row['wordSaid']
if prevWord != None and word != prevWord:
    start = prev
    end = row['timeStamp']
    duration = end - start
    repeats = nearest_1000(duration) // 1000
    per_sample_time = int(duration / repeats)
    for _ in range(repeats):
        curr_start = int(start + _ * per_sample_time)
        curr_end = int(start + (_ + 1) * per_sample_time)
        startEnd = startEnd.append([pd.Series([word, curr_start, curr_end, per_sample_time])])#, index=0)
    prev = end
prevWord = row['wordSaid']
startEnd.columns=["word", "start", "end", "duration"]
if startEnd.iloc[0]["duration"] < 750:
    length = startEnd.shape[0]
startEnd = startEnd.tail(length - 1)
startEnd = startEnd.reset_index()
startEnd = startEnd.drop(['index'], axis=1)
return startEnd

def make_dirs(startEnd, numChannels=8, root='.'):
    labels = startEnd["word"].unique()
    print(root)
    main_dir = os.path.join(root, "split_audio")
    print(main_dir)
    if not os.path.isdir(main_dir):
        os.mkdir(main_dir)
        for label in labels:
            subdir = os.path.join(main_dir, label)
if not os.path.isdir(subdir):
    os.mkdir(subdir)
for i in range(numChannels):
    channel_path = os.path.join(subdir, "ch{}".format(i + 1))
    if not os.path.isdir(channel_path):
        os.mkdir(channel_path)

def ms_to_strtime(ms):
    hours = ms // (3600000)
    minutes = (ms % 3600000) // 60000
    seconds = (ms % 60000) // 1000
    ms = ms % 1000
    return "{:02}:{:02}:{:02}.{:03}".format(hours, minutes, seconds, ms)

def timer(f, *args):
    print("Start: {}".format(datetime.now()))
    start = time()
    f(*args)
    end = time()
    duration = end - start
    print("Finished in {} seconds".format(duration))
    print("End: {}".format(datetime.now()))

def split_audio(startEnd, audio_dir, numChannels=8, root='.'):
    labels = startEnd["word"].unique()
    for file in [f for f in os.listdir(audio_dir) if f.endswith(".wav")]:
        labels = {label:0 for label in labels}
original_filepath = os.path.join(audio_dir, file)
print("\tProcessing {}".format(original_filepath))
channel = int(file[:2])
for i, row in startEnd.iterrows():
    if (i % VERBOSITY == 0):
        print("\t\tProcessed {}th clip".format(i))
    label = row["word"]
    startTime = ms_to_strtime(row["start"])
    endTime = ms_to_strtime(row["end"])
    subdir = "ch{}".format(channel)
    filename = "{:05}.wav".format(labels[label])
    labels[label] += 1
    new_filepath = os.path.join(root, "split_audio", label, subdir, filename)
    command = ["ffmpeg", "-i", original_filepath, "-ss", startTime, "-to", endTime, "-c", "copy", new_filepath]
    NULL = open(os.devnull, 'w')
    subprocess.run(command, stdout=NULL, stderr=NULL)

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        csv = sys.argv[1]
outputs = read_inputs(csv)
offset = first_signal(outputs)
outputs["timeStamp"] = outputs["timeStamp"] - offset
outputs = outputs[outputs.timeStamp > 0]
outputs = make_start_end_df(outputs)
print(outputs)
root = "/Users/42robotics/Documents/MindUI/jul02_2018_subvoc"
make_dirs(outputs, root=root)
timer(split_audio, outputs, root + "/original_audio", 8, root)
