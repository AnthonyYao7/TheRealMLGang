import os
import pandas as pd
import threading
from typing import List


def do_subset(entries: List) -> None:
    for entry in entries:
        try:
            os.system(f"yt-dlp -x --audio-format mp3 -o audios/{entry[0]}.mp3 {entry[1]} --verbose")
        except:
            pass


def main():

    done_ids = set([x.split('.')[0] for x in os.listdir("audios")])

    df = pd.read_csv("links.txt")
    df.columns = ["track_id", "Artist", "Track", "Link"]

    df.drop_duplicates(subset=["track_id"], inplace=True)

    print(len(df))

    df = df[~df['track_id'].isin(done_ids)]

    print(len(df))


    track_ids = list(df['track_id'])
    links = list(df['Link'])

    entries = list(zip(track_ids, links))

    partitions = 10
    partition_size = len(track_ids) // partitions + partitions

    threads = []

    for i in range(partitions):
        subset_entries = entries[i * partition_size: min((i + 1) * partition_size, len(track_ids))]
        thread = threading.Thread(target=do_subset, args=(subset_entries,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
