import pickle


def save_metadata(metadata, path):

    with open(path, "wb") as f:
        pickle.dump(metadata, f)


def load_metadata(path):

    with open(path, "rb") as f:
        return pickle.load(f)