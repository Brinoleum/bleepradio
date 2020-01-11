# library that automatically filters out the bad words
# i'm too lazy to make a dictionary for this

from better_profanity import profanity
import random
from google.cloud import texttospeech
import os
from tswift import Song

swear_replacements = [
        "bleezleborp", "plumbus", "atoteh", "boobasnot", "mychuno", 
        "litzergam", "dobbinips", "pobito", "dobana", "cotatod", "tocamok",
        "enolo", "kakotin"]

def retrieve_lyrics(artist_name, song_title):
    song = Song.find_song(artist_name + song_title)
    return song.lyrics

def test():
     s = Song('Taylor Swift', 'Love Story')
     s = Song.find_song('Love Story')
     print(s.lyrics)

# TODO: get the input from the user and feed that into the profanity filter
def process_lyrics(name):
    # making the assumption that the lyric input is one long string
    # and that nothing in the lyrics contains an asterisk
    # (actually because many censors use asterisks that might still work
    # if the music was already censored to an extent)
    profanity.load_censor_words()
    custom_profanity = ["nigger", "nigga"]
    profanity.add_censor_words(custom_profanity)
    lyrics = Song.find_song(name).lyrics
    print(lyrics)
    lyrics = profanity.censor(str(lyrics))

    def process_word(word):
        if '*' in word:
            word = random.choice(swear_replacements)
        return word

    return " ".join(process_word(word) for word in lyrics.split())

#process_lyrics("Love Story")

# this part is copy pasted from the online tutorial
# basically outputs the text as a sound file
def output_processed(processed):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=processed)
    voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL
            )

    audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3
            )
    #There is a delay of about a minute inbetween responses
    response=client.synthesize_speech(synthesis_input, voice, audio_config)
    with open('static/output.mp3', 'wb+') as out:
        out.write(response.audio_content)
        print('Audio content written to file output.mp3')
