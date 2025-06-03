import tkinter as tk
from tkinter import Menu
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import vlc
from tkinter import filedialog
import os
import configparser

# create a Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# create a Tkinter window
window = tk.Tk()
window.title("My Streaming App")

# create a menu bar
menu_bar = Menu(window)
window.config(menu=menu_bar)

# create a "Settings" menu
settings_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

def open_settings():
    settings_window = tk.Toplevel(window)
    settings_window.title("Settings")

    # add theme selection option
    tk.Label(settings_window, text="Theme:").grid(row=0, column=0)
    theme_var = tk.StringVar(value="Light")
    tk.OptionMenu(settings_window, theme_var, "Light", "Dark").grid(row=0, column=1)

    # add color selection option
    tk.Label(settings_window, text="Color:").grid(row=1, column=0)
    color_var = tk.StringVar(value="Blue")
    tk.OptionMenu(settings_window, color_var, "Blue", "Green", "Red").grid(row=1, column=1)

    # add launch at startup option
    launch_var = tk.BooleanVar(value=True)
    tk.Checkbutton(settings_window, text="Launch at startup", variable=launch_var).grid(row=2, column=0, columnspan=2)

    # create a function to save the settings
    def save_settings():
        # get the current settings values
        theme = theme_var.get()
        color = color_var.get()
        launch_on_start = launch_on_start_var.get()

        # save the settings to a file
        with open("settings.txt", "w") as f:
            f.write(f"theme:{theme}\n")
            f.write(f"color:{color}\n")
            f.write(f"launch_on_start:{launch_on_start}\n")

    # create a button to save the settings
    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack()

    settings_window.mainloop()

# create a label for the search box
search_label = tk.Label(window, text="Search for a song:")
search_label.pack()

# create an entry box for the user to enter the search query
search_entry = tk.Entry(window)
search_entry.pack()

# create a function to handle the search button click
def search():
    # get the user's search query
    query = search_entry.get()

    # search for the track
    results = sp.search(q=query, type='track')

    # display the results in a listbox
    results_listbox.delete(0, tk.END)
    for track in results['tracks']['items']:
        results_listbox.insert(tk.END, f"{track['name']} by {track['artists'][0]['name']}")

# create a button to trigger the search
search_button = tk.Button(window, text="Search", command=search)
search_button.pack()

# create a label for the results box
results_label = tk.Label(window, text="Results:")
results_label.pack()

# create a listbox to display the search results
results_listbox = tk.Listbox(window)
results_listbox.pack()

# create a function to handle the add button click
def add():
    # get the selected track from the results listbox
    selected_track = results_listbox.get(tk.ACTIVE)

    # extract the track name and artist name
    track_name, artist_name = selected_track.split(" by ")

    # search for the track again to get its ID
    results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track')
    track_id = results['tracks']['items'][0]['id']

    # add the track to the user's playlist
    playlist_id = 'YOUR_PLAYLIST_ID'
    sp.user_playlist_add_tracks(user='YOUR_USERNAME', playlist_id=playlist_id, tracks=[track_id])

# create a button to trigger the add
add_button = tk.Button(window, text="Add to Playlist", command=add)
add_button.pack()

# create a label for the playlist box
playlist_label = tk.Label(window, text="Playlist:")
playlist_label.pack()

# create a listbox to display the user's playlist
playlist = []
playlist_box = tk.Listbox(window)
playlist_box.pack()

# load saved playlist if available
try:
    with open("playlist.txt", "r") as f:
        playlist = f.read().splitlines()
except FileNotFoundError:
    pass

playlist_box.delete(0, tk.END)
for song in playlist:
    playlist_box.insert(tk.END, song)

# create a MusicPlayer class

config = configparser.ConfigParser()
config.read('config.ini')

class MusicPlayer:
    def __init__(self, master):
        # load the configuration file
        config.read('config.ini')
        self.directory = config.get('DEFAULT', 'directory', fallback=os.getcwd())
        self.master = master
        master.title("Music Player")

        # Create VLC instance
        self.vlc_instance = vlc.Instance('--no-xlib')

        # Initialize player
        self.player = self.vlc_instance.media_player_new()

        # Create buttons
        self.play_button = tk.Button(master, text="Play", command=self.play)
        self.pause_button = tk.Button(master, text="Pause", command=self.pause)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop)

        # Create volume slider
        self.volume_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)

        # Create position slider
        self.position_slider = tk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_position)

        # Create label for song information
        self.song_info_label = tk.Label(master, text="")

        # create a button to open the directory in the file explorer
        self.open_button = tk.Button(master, text="Open Directory", command=self.open_directory)
        self.open_button.grid(row=4, column=0, columnspan=3)

        # Position elements on the window
        self.play_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=1)
        self.stop_button.grid(row=0, column=2)
        self.volume_slider.grid(row=1, column=0, columnspan=3, sticky=tk.EW)
        self.position_slider.grid(row=2, column=0, columnspan=3, sticky=tk.EW)
        self.song_info_label.grid(row=3, column=0, columnspan=3)

    def play(self):
        # get the selected song from the playlist box
        selected_song = playlist_box.get(tk.ACTIVE)

        # open the audio file using VLC
        media = self.vlc_instance.media_new(selected_song)

        # set the media to the player and play it
        self.player.set_media(media)
        self.player.play()

        # update the song info label
        self.song_info_label.config(text=f"Now playing: {selected_song}")

    def pause(self):
        # pause the currently playing song
        self.player.pause()

    def stop(self):
        # stop the currently playing song
        self.player.stop()

    def set_volume(self, value):
        # set the volume of the player
        self.player.audio_set_volume(int(value))

    def set_position(self, value):
        # set the position of the player
        self.player.set_position(float(value) / 100)

def select_directory():
    # prompt the user to select a directory
    directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory")
    # set the directory in the config file
    config.set('DEFAULT', 'directory', directory)
    with open('config.ini', 'w') as f:
        config.write(f)
    # update the directory label
    directory_label.config(text=f"Directory: {directory}")

# create a button to trigger the directory selection
directory_button = tk.Button(window, text="Select Directory", command=select_directory)
directory_button.pack()

# create a label to display the selected directory
directory_label = tk.Label(window, text="")
directory_label.pack()


# create a music player window
music_player_window = tk.Toplevel(window)
music_player = MusicPlayer(music_player_window)

# start the main event loop
window.mainloop()