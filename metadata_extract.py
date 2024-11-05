import os
import pandas as pd
import json
import numpy as np
import gc
import re
import pickle

# test_dict = {"a": 1, "b": {"c": 2}}

# np.save("test_dict.npy", test_dict)

# d = np.load("test_dict.npy", allow_pickle=True).item()

file_list = os.listdir("./metadata/keyframes")

file_list = list(
    map(
        lambda x: x.split(".")[0],
        file_list
    )
)

metadata_dict = dict()

for f in file_list:
    df = pd.read_csv(f"./metadata/keyframes/{f}.csv")
    with open(f"./metadata/youtube_metadata/{f}.json") as j:
        u_data = json.load(j)

    fps = df["fps"]
    video_url = re.sub(r"(.*watch\?v=)(.*)", r"\2", u_data["watch_url"])

    if fps[1] != fps.mean():
        print(f"Inconsistent fps {f}")

    metadata_dict[f] = [fps[0], str(video_url)]

    del df
    gc.collect()


with open("./db/video_metadata.pkl", "wb") as file:
    pickle.dump(metadata_dict, file)

np.save("./db/video_metadata.npy", metadata_dict, allow_pickle=True)
