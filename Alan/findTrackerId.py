import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_track_id(artist, song, data):
    artist_matches = process.extract(artist, data['artists'], limit=10, scorer=fuzz.token_sort_ratio)
    best_artist_match = artist_matches[0]

    if best_artist_match[1] >= 90:
        artist_filtered_data = data[data['artists'] == best_artist_match[0]]
    else:
        artist_filtered_data = data

    song_matches = process.extract(song, artist_filtered_data['track_name'], limit=1, scorer=fuzz.token_sort_ratio)
    best_song_match = song_matches[0]

    track_id = artist_filtered_data.loc[artist_filtered_data['track_name'] == best_song_match[0]]['track_id'].values[0]
    return track_id

if __name__ == "__main__":
    data = pd.read_csv('cleaned_data.csv')

    artist_name = input("Enter artist name: ")
    song_name = input("Enter song name: ")

    result_track_id = find_track_id(artist_name, song_name, data)
    print("The track ID is:", result_track_id)