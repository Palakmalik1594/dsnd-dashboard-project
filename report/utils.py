from pathlib import Path
import pickle


# Project root path
ROOT_PATH = Path(__file__).resolve().parent.parent

# model.pkl path
MODEL_PATH = ROOT_PATH / "assets" / "model.pkl"


def load_model():

    with open(MODEL_PATH, "rb") as file:

        model = pickle.load(file)

    return model