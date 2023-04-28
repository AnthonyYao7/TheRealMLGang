import csv
from Levenshtein import distance

def find_track_id(artist, song, dataset):
    min_distance = float('inf')
    track_id = None
    similar_artist = ""
    similar_song = ""

    with open(dataset, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        for row in reader:
            current_track_id, current_artist, current_song = row
            if current_artist == artist and current_song == song:
                return current_track_id
            else:
                current_distance = distance(song.lower(), current_song.lower())
                if current_distance < min_distance:
                    min_distance = current_distance
                    track_id = current_track_id
                    similar_artist = current_artist
                    similar_song = current_song

    return track_id, similar_artist, similar_song

artist = input("Enter artist name: ")
song = input("Enter song name: ")
dataset = "cleaned_data.csv"

track_id, similar_artist, similar_song = find_track_id(artist, song, dataset)

if track_id:
    print(f"Found track id: {track_id}")
    if similar_artist != artist or similar_song != song:
        print(f"Most similar song: {similar_artist} - {similar_song}")
else:
    print("No track found.")
