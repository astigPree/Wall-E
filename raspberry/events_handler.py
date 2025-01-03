from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
 

class MusicEventsHandler:
    
    current_token : str = None
    
    def get_token(self):
        auth_string = CLIENT_ID + ":" + CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str( base64.b64encode(auth_bytes) , 'utf-8' )
         
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data =  {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        self.current_token = token
        return token
    
    
    def get_auth_header(self):
        return {"Authorization": "Bearer " + self.current_token}











import yt_dlp as youtube_dl

def get_audio_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'skip_download': True,  # This prevents downloading the file
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{song_name}", download=False)
        audio_url = info['entries'][0]['url']
        return audio_url

# Example Usage
song_name = "Never Gonna Give You Up"
audio_url = get_audio_url(song_name)

print("Audio URL:", audio_url)
