import json
import math
import time
import tkinter as tk
import ctypes

#window settings
ctypes.windll.shcore.SetProcessDpiAwareness(1)
window = tk.Tk()
window.tk.call('tk', 'scaling', 1.0) # Adjust the value as needed
window.title("Spotify Data Analysis")
window.geometry("600x600")
window.configure(bg="black")
window.resizable(False, False)

# File List
file_paths = [
    "Streaming_History_Audio_2019-2023_0.json",
    "Streaming_History_Audio_2023-2024_1.json",
    "Streaming_History_Audio_2024-2025_2.json",
    "Streaming_History_Audio_2025_3.json"
]

# Function to read JSON data from a file
def read_json(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from the file {file_path}.")
    return None

def streamtime():
    print("CALCULATING TOTAL STREAMING TIME...")
    loading()
    total = 0
    for file_path in file_paths:
        json_data = read_json(file_path)
        if json_data:
            for obj in json_data:
                total = total + obj.get("ms_played", 0)
    total = total/60000 #converts the total from milliseconds to minutes
    totalInt = math.trunc(total) #converts the total to an integer
    totalDecimal = total - totalInt #gets the decimal part of the total
    print("TOTAL STREAMING TIME:", totalInt, "MINUTES AND", math.floor(totalDecimal*60), "SECONDS") #prints the total of all the ms_played values in the json file

def artistlistened():
    initialartists = []
    seen = set()
    artistlistened = []
    for file_path in file_paths:
        json_data = read_json(file_path)
        if json_data:
            for obj in json_data:
                initialartists.append(obj.get("master_metadata_album_artist_name", 0))
    for artist in initialartists:
        if artist not in seen:
            seen.add(artist)
            artistlistened.append(artist)
    return artistlistened

def trackslistened():
    initialtracks = []
    seen = set()
    trackslistened = []
    for file_path in file_paths:
        json_data = read_json(file_path)
        if json_data:
            for obj in json_data:
                initialtracks.append(obj.get("master_metadata_track_name", 0))
    for track in initialtracks:
        if track not in seen:
            seen.add(track)
            trackslistened.append(track)
    return trackslistened

def firsttimetrack(track, artist):
    for file_path in file_paths:
        json_data = read_json(file_path)
        if json_data:
            for obj in json_data:
                if obj.get("master_metadata_track_name", 0) == track and obj.get("master_metadata_album_artist_name", 0) == artist:
                    return obj.get("ts", 0) #returns the timestamp of the first time the track was played
    return None

def firsttimeartist(artist):
    for file_path in file_paths:
        json_data = read_json(file_path)
        if json_data:
            for obj in json_data:
                if obj.get("master_metadata_album_artist_name", 0) == artist:
                    return obj.get("ts", 0) #returns the timestamp of the first time the artist was played
    return None

def loading():
    for i in range(5):
        time.sleep(0.4)
        print("...")
    time.sleep(0.4)

if __name__ == "__main__":
    choice = input("WHAT WOULD YOU LIKE TO DO?\n(1) CALCULATE TOTAL STREAMING TIME\n(2) CALCULATE NUMBER OF ARTISTS LISTENED TO\n(3) CALCULATE NUMBER OF TRACKS LISTENED TO\n(4) FIND THE FIRST TIME A TRACK WAS PLAYED\n(5) FIND THE FIRST TIME AN ARTIST WAS PLAYED\n(9) EXIT\n --> ")
    if choice == "1":
        streamtime()
    elif choice == "2":
        artists = artistlistened()
        print("CALCULATING NUMBER OF ARTISTS LISTENED TO...")
        loading()
        print("NUMBER OF ARTISTS LISTENED TO:", len(artists))
    elif choice == "3":
        tracks = trackslistened()
        print("CALCULATING NUMBER OF TRACKS LISTENED TO...")
        loading()
        print("NUMBER OF TRACKS LISTENED TO:", len(tracks))
    elif choice == "4":
        track = input("ENTER THE NAME OF THE TRACK: ")
        artist = input("ENTER THE NAME OF THE ARTIST: ")
        firsttime = firsttimetrack(track, artist)
        print("FINDING THE FIRST TIME THAT TRACK WAS PLAYED...")
        loading()
        if firsttime:
            print("FIRST TIME PLAYED:", firsttime)
        else:
            print("TRACK NOT FOUND!")
    elif choice == "5":
        artist = input("ENTER THE NAME OF THE ARTIST: ")
        firsttime = firsttimeartist(artist)
        print("FINDING THE FIRST TIME THAT ARTIST WAS PLAYED...")
        loading()
        if firsttime:
            print("FIRST TIME PLAYED:", firsttime)
        else:
            print("ARTIST NOT FOUND!")
    elif choice == "9":
        print("GOODBYE!")
        exit()
    else: 
        print("INVALID INPUT! PLEASE TRY AGAIN.")
        exit()

label = tk.Label(window, text="Spotify Data Analysis", font=("Arial", 40), bg="black", fg="green")
label.pack(pady=20)

button1 = tk.Button(window, text="Calculate Total Streaming Time", font=("Arial", 20), bg="black", fg="green", command=lambda: streamtime())
button1.pack(pady=10)