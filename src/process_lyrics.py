# library that automatically filters out the bad words
# i'm too lazy to make a dictionary for this

from better_profanity import profanity
import random
from google.cloud import texttospeech

swear_replacements = [
        "bleezleborp", "plumbus", "atoteh", "boobasnot", "mychuno", 
        "litzergam", "dobbinips"]

# TODO: get the input from the user and feed that into the profanity filter
def process_lyrics(lyrics):
    # making the assumption that the lyric input is one long string
    # and that nothing in the lyrics contains an asterisk
    # (actually because many censors use asterisks that might still work
    # if the music was already censored to an extent)
    profanity.load_censor_words()

    lyrics = profanity.censor(lyrics)

    def process_word(word):
        if '*' in word:
            word = random.choice(swear_replacements)
        return word

    return " ".join(process_word(word) for word in lyrics.split())

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

    response=client.synthesize_speech(synthesis_input, voice, audio_config)

    with open('audio/output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file output.mp3')
