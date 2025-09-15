# SpotiDownloader

Downloads Spotify music via YouTube

## Installation

1. Download the GitHub repository by running the following command in your Terminal
   ```bash
   git clone https://github.com/AJ-Holzer/SpotToYT
   ```
2. Run `pip install -r requirements.txt` in terminal
3. Set up Spotify credentials:
   1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   2. Click **Create App** -> give it a name (e.g. "Playlist Transfer")
   3. Add a Redirect URI:
      - Example: `http://127.0.0.1:8888/callback`
      - This is where Spotify will send the user after login
   4. Select `Web API`
4. Insert the Spotify client id and client secret in the `.env` file
5. Add a redirect URL in the `.env` file (e.g. `http://127.0.0.1:8888/callback`). This is where Spotify will send the user after login

## Usage

1. Run the `main.py` file located in the `src` folder using this command:
   ```bash
   python src/main.py
   ```
   or using a 'precompiled' binary from the [latest release](https://github.com/AJ-Holzer/SpotiDownloader/releases/latest)
2. Enter your Spotify playlist or track URL
3. Now your music will be downloaded!

## Incoming

- Beautiful GUI using [Flet](https://flet.dev)

---

_😊 If you like what you see, drop a star and check out my [Website](https://ajservers.site). Thank You ♥️_
