import numpy as np
import streamlit as st


def group_by_video(results):
    gr = dict()
    for d in results:
        index = d[2].item() * 1000 + d[3].item()

        vid_bin = gr.get(index, list())

        vid_bin.append(d)

        gr[index] = vid_bin

    return sorted(
        gr.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )


def group_occurence(indices: np.ndarray
                    ) -> tuple[np.ndarray, np.ndarray]:
    return np.unique(indices, return_counts=True)


def group_by_occurence(results) -> dict:
    conf_bin = dict()

    # for result in results:
    for f in results:
        fbin = conf_bin.get(f[0], list())
        fbin.append(f)
        conf_bin[f[0]] = fbin

    return sorted(
        conf_bin.items(),
        key=lambda x: x[0],
        reverse=True
    )


def get_nearby(f,
               k,
               nearby_index_list):
    output = list()
    output.append([
        f[0],
        f[1],
        f[2],
        f[3],
        f[4],
        True
    ])

    if k == 0:
        return output

    nearby_list = nearby_index_list[f[2]-1][f[3]-1]
    cf_index = f[1]

    left_bound = max(
        0,
        cf_index - k
    )
    right_bound = min(
        len(nearby_list)-1,
        cf_index + k
    )

    for l in range(left_bound, cf_index):
        f = [
            f[0],
            l,
            f[2],
            f[3],
            nearby_list[l],
            False
        ]
        if f not in output:
            output.append(f)

    for r in range(cf_index+1, right_bound+1):
        f = [
            f[0],
            r,
            f[2],
            f[3],
            nearby_list[r],
            False
        ]
        output.append(f)

    return output


def paging(results, k):
    output = []
    size_left = k
    cb = []

    for b in results:
        bin_len = len(b[1])

        if (bin_len > size_left):
            if size_left != k:
                output.append(cb)

                size_left = k
                cb = []

        if bin_len <= size_left:
            cb.append([b[0], b[1]])
            size_left -= bin_len
            continue
        else:
            split_chunk, _ = divmod(bin_len, k)

            for j in range(split_chunk+1):
                start_range = j * k

                splited_bin = [[b[0], b[1][start_range:start_range+k]]]
                output.append(splited_bin)

            size_left = k
    if cb:
        output.append(cb)

    return output
