# MoodMusic
A program that recommends songs to users based on their current mood as well as their top artists/tracks on Spotify.

Utilizes Deepface for facial recognition on the user's current emotion, and Spotify API to pull the user's top artists and tracks.

## How to run
Make sure you have the necessary packages (`deepface`, `cv2`, `matplotlib`, `keyboard`, `bottle`, `spotipy` and `time`) installed first, then run the program. Then navigate to `http://localhost:8080`, where you'll be asked to login with Spotify. After logging in, the webcam should turn on, and your current mood shoud be recognized by the program. Press 'g' to exit the webcam window, and your recommended songs should be outputted. The webcam window also automatically closes after a few seconds.
