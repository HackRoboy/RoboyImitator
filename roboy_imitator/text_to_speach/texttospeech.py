'''
After you've set your subscription key, run this application from your working
directory with this command: python TTSSample.py
'''
import os, requests, time
from xml.etree import ElementTree

# This code is required for Python 2.7
try: input = raw_input
except NameError: pass

'''
If you prefer, you can hardcode your subscription key as a string and remove
the provided conditional statement. However, we do recommend using environment
variables to secure your subscription keys. The environment variable is
set to SPEECH_SERVICE_KEY in our sample.
For example:
subscription_key = "Your-Key-Goes-Here"
'''

#if 'SPEECH_SERVICE_KEY' in os.environ:
#    subscription_key = os.environ['SPEECH_SERVICE_KEY']
#else:
#    print('Environment variable for your subscription key is not set.')
#    exit()
# hardcode subscription key
# subscription_key = ""
# config subscription key

voice_dict = {
    "Michael": "(de-AT, Micheal)",
    "Karsten": "(de-CH, Karsten)",
    "Hedda": "(de-DE, Hedda)",
    "HeddaRus": "(de-DE, HeddaRUS)",
    "Stefan": "(de-DE, Stefan, Apollo)",
    "Catherine": "(en-AU, Catherine)",
    "Hayley": "(en-AU, HayleyRUS)",
    "Linda": "(en-CA, Linda)",
    "Heather": "(en-CA, HeatherRUS)",
    "Susan": "(en-GB, Susan, Apollo)",
    "Hazel": "(en-GB, HazelRUS)",
    "George": "(en-GB, George, Apollo)",
    "Sean": "(en-IE, Sean)",
    "Heera": "(en-IN, Heera, Apollo)",
    "Priya": "(en-IN, PriyaRUS)",
    "Ravi": "(en-IN, Ravi, Apollo)",
    "Zira": "(en-US, ZiraRUS)",
    "Jessa": "(en-US, JessaRUS)",
    "Benjamin": "(en-US, BenjaminRUS)",
    "Jessa": "(en-US, Jessa24kRUS)",
    "Guy": "(en-US, Guy24kRUS)"
}

class TextToSpeech(object):
    def __init__(self, subscription_key, tts_string):
        self.subscription_key = subscription_key
        # self.tts = input("What would you like to convert to speech: ")  # input via __init__ call (tts_string
        self.tts = tts_string
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    '''
    The TTS endpoint requires an access token. This method exchanges your
    subscription key for an access token that is valid for ten minutes.
    '''
    def get_token(self):
        fetch_token_url = "https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self, voice):
        base_url = 'https://westus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        voice_name = 'Microsoft Server Speech Text to Speech Voice ' + voice
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'de-DE')
        # change Jessa to guy for male voice
        voice.set('name', voice_name)
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        '''
        If a success response is returned, then the binary audio is written
        to file in your working directory. It is prefaced by sample and
        includes the date.
        '''
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")

def tts_test(subscription_key, teststring, voice_name = "Guy"):
    voice = voice_dict[voice_name]
    app = TextToSpeech(subscription_key, teststring)
    app.get_token()
    app.save_audio(voice=voice)


if __name__ == "__main__":
    tts_test(subscription_key, "Das ist österreichisch", voice_name="Karsten")