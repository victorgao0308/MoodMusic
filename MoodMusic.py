# https://github.com/plamere/spotipy/blob/master/spotipy/util.py
# http://www.acmesystems.it/python_httpd
import cv2
from deepface import DeepFace as df
import matplotlib.pyplot as plt
import keyboard
from bottle import route, run, request
import spotipy
from spotipy import oauth2
import time


PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '5e38362c53e647ff8a3d62e242626e3c'
SPOTIPY_CLIENT_SECRET = '490ea6cdd2454ade9f25783489c21e72'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-top-read'
CACHE = '.spotipyoauthcache'

topArtistURLs = []
topGenres = []
topTrackURLs = []

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE, cache_path=CACHE)

@route('/')
def index():
        
    access_token = ""

    token_info = sp_oauth.get_access_token()

 
    url = request.url
    code = sp_oauth.parse_response_code(url)
    if code != url:
        print("Found Spotify auth code in Request URL! Trying to get valid access token...")
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        for artist in sp.current_user_top_artists(limit=2)["items"]:
            topArtistURLs.append(artist["external_urls"]["spotify"])
            topGenres.append(artist["genres"][0])
        #get user's top 3 tracks
        for track in sp.current_user_top_tracks(limit=5)["items"]:
            topTrackURLs.append(track["external_urls"]["spotify"])
        print(topArtistURLs)
        def GetSongRec(emotion, topArtistss, topGenress, topTrackss):
            targetValence = .5
            minValence = 0
            maxValence= 1
            targetDanceability = .5
            minDanceability = 0
            maxDanceability = 1
            targetEnergy = 0.5
            minEnergy = 0
            maxEnergy = 1
            targetInstrumentalness = 0.5
            minInstrumentalness = 0
            maxInstrumentalness = 1
            if(emotion == "angry"):
                targetValence = .2
                minValence = 0
                maxValence= .4
                targetDanceability = .25
                minDanceability = 0
                maxDanceability = 1
                targetEnergy = .8
                minEnergy = .25
                maxEnergy = 1
                targetInstrumentalness = 0.5
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "happy"):
                targetValence = .8
                minValence = .5
                maxValence= 1
                targetDanceability = .75
                minDanceability = .1
                maxDanceability = 1
                targetEnergy = .7
                minEnergy = .2
                maxEnergy = 1
                targetInstrumentalness = 0.7
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "sad"):
                targetValence = .1
                minValence = 0
                maxValence= .3
                targetDanceability = 0.2
                minDanceability = 0
                maxDanceability = .8
                targetEnergy = .2
                minEnergy = 0
                maxEnergy = 1
                targetInstrumentalness = 0.5
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "disgust"):
                targetValence = .3
                minValence = 0
                maxValence= .5
                targetDanceability = .1
                minDanceability = 0
                maxDanceability = 1
                targetEnergy = .25
                minEnergy = .1
                maxEnergy = .9
                targetInstrumentalness = 0.5
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "fear"):
                targetValence = .8
                minValence = 0.5
                maxValence= 1
                targetDanceability = .2
                minDanceability = 0.1
                maxDanceability = 1
                targetEnergy = 0.3
                minEnergy = .1
                maxEnergy = 1
                targetInstrumentalness = 0.85
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "surprise"):
                targetValence = .6
                minValence = 0.4
                maxValence= .9
                targetDanceability = .35
                minDanceability = .1
                maxDanceability = .95
                targetEnergy = 0.5
                minEnergy = .1
                maxEnergy = 1
                targetInstrumentalness = 0.5
                minInstrumentalness = 0
                maxInstrumentalness = 1
            elif(emotion == "neutral"):
                targetValence = .5
                minValence = 0
                maxValence= 1
                targetDanceability = .5
                minDanceability = 0
                maxDanceability = 1
                targetEnergy = 0.5
                minEnergy = 0
                maxEnergy = 1
                targetInstrumentalness = 0.5
                minInstrumentalness = 0
                maxInstrumentalness = 1
            recs = sp.recommendations(seed_artists=topArtistss, topGenres=topGenress, topTrackURLs=topTrackss, limit=10, max_valence = maxValence, max_danceability = maxDanceability,max_energy = maxEnergy, max_intrumentalness = maxInstrumentalness, min_valence = minValence, min_danceability = minDanceability, min_energy = minEnergy, min_instrumentalness = minInstrumentalness, target_danceability = targetDanceability, target_energy = targetEnergy,
target_instrumentalness = targetInstrumentalness, target_valence = targetValence)
            for track in recs['tracks']:
                artistString = ""
                for artist in track['artists']:
                    if(artistString != ""):
                        artistString = artistString +", "
                    artistString = artistString + str(artist['name'])
                print(track['name']+ " - " + artistString)
            print(emotion)
            if(len(recs['tracks']) <1):
                print("No available recommendations!")
            cv2.destroyAllWindows()
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError ("Cannot Open Camera!")
        oldTime = time.time()
        while True:
            ret,frame = cap.read()
            result = df.analyze(frame,actions = ['emotion'], enforce_detection = False)
            emote = result['dominant_emotion']
            DisplayText = emote
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,1.1,4)
            for(x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w, y+h), (0,255,0),2)
            font = cv2.FONT_HERSHEY_PLAIN
            cv2.putText(frame, DisplayText, (50,50), font, 3, (0,0,0), 2, cv2.LINE_4)
            cv2.imshow('Original video',frame)
            if(time.time()-oldTime >=8):
                GetSongRec(result['dominant_emotion'],topArtistURLs,topGenres, topTrackURLs)
                break
            inpkey = cv2.waitKey(2)&0xFF
            if(inpkey == ord('q')):
                break
            elif(inpkey == ord('g')):
                GetSongRec(result['dominant_emotion'],topArtistURLs,topGenres, topTrackURLs)
                break
        cv2.destroyAllWindows()
        return "Login Successful!"
    else:
        return htmlForLoginButton()
def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='', port=8080)

