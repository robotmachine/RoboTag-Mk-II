import os
import eyed3
import json
import logging


def main():
    config = get_config()
    #logger = create_logger()
    music_root = config_parse(config, ['music_root', 'path'])
    path_data = os.getcwd().replace(f'{music_root}/', '').split('/')

    # Get all .mp3 files in current dir
    dir_contents = os.listdir(os.getcwd())
    music_files = [x for x in dir_contents if '.mp3' in x]
    music_files.sort()

    album_info = get_album_data(path_data)
    tracks = build_tracks(music_files)
    write_tags(album_info, music_files, tracks)
    quit()

class AlbumInfo:
    def __init__(self, album_data, path_data):
        try:
            self.title = album_data['title'].strip()
        except KeyError:
            self.title = path_data[1][5:].strip()
        try:
            self.year = album_data['year'].strip()
        except KeyError:
            self.year = path_data[1][:4].strip()
        try:
            self.artist = album_data['artist'].strip()
        except KeyError:
            self.artist = path_data[0].strip()
        try:
            self.album_artist = album_data['album_artist'].strip()
        except KeyError:
            self.album_artist = path_data[0].strip()
        try:
            self.tracks = album_data['tracks']
        except KeyError:
            self.tracks = {}

    def write_album_data(self, album_data_fname):
        json_data = json.dumps(self, indent=4)
        with open(album_data_fname, 'w') as file:
            file.write(json_data)


def get_config():
    config_file_name = 'rt_config.json'
    config = None
    try:
        # Check CWD for a config file
        config = json.load(open(f"{os.getcwd()}/{config_file_name}"))
    except FileNotFoundError:
        try:
            # Check dir where the script is running for a config file
            config = json.load(open(f"{os.path.dirname(__file__)}/{config_file_name}"))
        except FileNotFoundError:
            try:
                # Check user's home folder for config file
                config = json.load(open(f"{os.path.expanduser('~')}/{config_file_name}"))
            except FileNotFoundError:
                quit('No config file found')
    return config


def config_parse(config, query):
    if query[1] == 'path':
        try:
            config_query = os.path.expanduser(config[query[0]])
            if os.path.exists(config_query):
                return config_query
            else:
                return False
        except KeyError:
            quit(f'{query} not set in config')
    elif query[1] == 'None':
        return False


def create_logger():
    logger = logging.getLogger("safarijim")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = logging.FileHandler(filename=f'.robotag.log', mode="a")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def get_album_data(path_data):
    # File in CWD that contains album info
    album_data_filename = '.album_info.json'
    try:
        album_data = json.load(open(album_data_filename))
    except json.decoder.JSONDecodeError:
        album_data = {}
    except FileNotFoundError:
        album_data = {}
    album_info = AlbumInfo(album_data, path_data)
    return album_info


def build_tracks(music_files):
    # Create empty array for tracks
    tracks = {}
    # Loop through .mp3 files and build array
    for mp3_file in music_files:
        # Single disc filename should be Eg. "01 Track Name.mp3"
        if mp3_file[2] == ' ':
            track_number = mp3_file[:2]
            disc_number = '01'
            track_name = mp3_file[3:].replace('.mp3', '')
            try:
                tracks[f'disc{disc_number}']
            except KeyError:
                tracks[f'disc{disc_number}'] = {}
            tracks[f'disc{disc_number}'][f'track{track_number}'] = track_name
        # Multi disc filename should be Eg. "01-02 Track Name.mp3"
        elif mp3_file[2] == '-':
            track_number = mp3_file[3:5]
            disc_number = mp3_file[:2]
            track_name = mp3_file[6:].replace('.mp3', '')
            try:
                tracks[f'disc{disc_number}']
            except KeyError:
                tracks[f'disc{disc_number}'] = {}
            tracks[f'disc{disc_number}'][f'track{track_number}'] = track_name
        # Catch-all in case it's something else, but it won't work too good
        else:
            track_number = None
            disc_number = None
            track_name = mp3_file.replace('.mp3', '')
            try:
                tracks[f'disc{disc_number}']
            except KeyError:
                tracks[f'disc{disc_number}'] = {}
            tracks[f'disc{disc_number}'][f'track{track_number}'] = track_name
    return tracks


def write_tags(album_info, music_files, tracks):
    for music_file in music_files:
        loaded_file = eyed3.load(music_file)
        print(f'{loaded_file.tag.title} by {loaded_file.tag.artist} on the album {loaded_file.tag.album}')
    return True


if __name__ == "__main__":
    main()
