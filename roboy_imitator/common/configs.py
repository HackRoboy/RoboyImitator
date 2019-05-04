from pathlib import Path

import yaml

CONFIGS_PATH = Path("../../configs/secrets.yaml")

with open(CONFIGS_PATH) as stream:
    CONFIGS = yaml.safe_load(stream)

VOICES = {
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
    "Hazel": "(en-GB, HazelRUS)",  # fear
    "George": "(en-GB, George, Apollo)",
    "Sean": "(en-IE, Sean)",
    "Heera": "(en-IN, Heera, Apollo)",
    "Priya": "(en-IN, PriyaRUS)",
    "Ravi": "(en-IN, Ravi, Apollo)",
    "Zira": "(en-US, ZiraRUS)",  # neutral
    "Jessa": "(en-US, JessaRUS)",  # contempt
    "Benjamin": "(en-US, BenjaminRUS)", # happiness
    "Jessa2": "(en-US, Jessa24kRUS)", # anger
    "Guy": "(en-US, Guy24kRUS)" # surprise
}

EMOTIONS = {
    "neutral": "Zira",
    "contempt": "Jessa",
    "happiness": "Benjamin",
    "anger": "Jessa2",
    "surprise": "Guy",
    "fear": "Hazel",
    "sadness": "Susan",
    "disgust": "Sean"
}
