from vosk import Model
import os

MODEL_DIR = "vosk-model"

if not os.path.exists(MODEL_DIR):
    raise Exception("Vosk model not found.")

model = Model(MODEL_DIR)