import pandas as pd
import sys

def read_inputs(file):
    outputs = pd.read_csv(file, sep=',')
    return outputs

def first_signal(df):
    return df.iloc[0]["timeStamp"]

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        csv = sys.argv[1]
outputs = read_inputs(csv)
offset = first_signal(outputs)
outputs["timeStamp"] = outputs["timeStamp"] - offset
print(outputs)
outputs.to_csv("outputs_adjusted.csv")
