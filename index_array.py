import numpy as np
import re
import os
import json
import pickle

indexes = np.load("./db/index_compact_2.npy")


def decode(index_compact):
    index, frame = divmod(index_compact, 1000000)
    index, video = divmod(index, 1000)
    index, folder = divmod(index, 100)

    return [index, folder, video, frame]


current_set = 0
current_vid = 0

output = list()

set_bin = list()

sets = sorted(os.listdir("./keyframes"))

for s in sets:
    vids = sorted(os.listdir(f"./keyframes/{s}"))
    offset = 1
    set_bin = list()
    for i, v in enumerate(vids):
        v_id = int(re.sub(r"L.._V(...)", r"\1", v))

        missing_index = i+offset
        if missing_index != v_id:
            for j in range(v_id-missing_index):
                set_bin.append(None)
                offset += 1

        kf_list = os.listdir(f"./keyframes/{s}/{v}")

        kf_list = sorted(list(
            map(
                lambda x: int(x.split(".")[0]),
                kf_list
            )
        ))

        set_bin.append(kf_list)
    output.append(set_bin)

with open("./db/index_frame.pkl", "wb") as f:
    pickle.dump(output, f)
