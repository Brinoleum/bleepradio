# library that automatically filters out the bad words
# i'm too lazy to make a dictionary for this

from better_profanity import profanity
import random
from google.cloud import texttospeech
from tswift import Song
import os


def retrieve_lyrics(artist_name, song_title):
    song = Song.find_song(artist_name + song_title)
    return song.lyrics


def test():
    s = Song('Taylor Swift', 'Love Story')
    s = Song.find_song('Love Story')
    print(s.lyrics)

def random_bgm():
    dir = "static/audio"
    filename = random.choice(os.listdir(dir))

    return str(filename)

class NoCuss:
    def __init__(self, songName):
        self.songName = songName
        swear_replacements = [
            "bleezleborp", "plumbus", "atoteh", "boobasnot", "mychuno",
            "litzergam", "dobbinips", "pobito", "dobana", "cotatod", "tocamok",
            "enolo", "kakotin"]
        self.swear_replacements = swear_replacements
        custom_profanity = ["nigger", "nigga", "niggaz", "dicks", "niggas", "muthafucka", "chickenshit", "muthafuckin", "assed"\
                            , "assho", "motherfuckin'", "ho", "hoes", "fuckin'", "runnin'ass", "hoesass", "bitch'll"]
        self.custom_profanity = custom_profanity

    def process_word(self, word):
        if '*' in word:
            word = random.choice(self.swear_replacements)
        return word

    # TODO: get the input from the user and feed that into the profanity filter
    def process_lyrics(self):
        # making the assumption that the lyric input is one long string
        # and that nothing in the lyrics contains an asterisk
        # (actually because many censors use asterisks that might still work
        # if the music was already censored to an extent)
        profanity.load_censor_words()

        profanity.add_censor_words(self.custom_profanity)
        lyrics = Song.find_song(self.songName).lyrics
        print(lyrics)
        lyrics = profanity.censor(str(lyrics))

        return " ".join(self.process_word(word) for word in lyrics.split())

    # this part is copy pasted from the online tutorial
    # basically outputs the text as a sound file
    def output_processed(self, processed):
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=processed)
        voice = texttospeech.types.VoiceSelectionParams(
                language_code='en-US',

                ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE
                )

        audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3
                )
        #There is a delay of about a minute inbetween responses
        response=client.synthesize_speech(synthesis_input, voice, audio_config)
        with open('static/output.mp3', 'wb+') as out:
            out.write(response.audio_content)
            print('Audio content written to file output.mp3')

    def song_name(self):
        profanity.load_censor_words()

        profanity.add_censor_words(self.custom_profanity)
        title = str(Song.find_song(self.songName).title)
        title = profanity.censor(str(title))

        return " ".join(self.process_word(word) for word in title.split())