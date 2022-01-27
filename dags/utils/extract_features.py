import os, errno
from typing import Any

import librosa
import numpy as np
import os
import logging

LOGGER = logging.getLogger(__name__)


def extract_features(
    input_folder: str, output_folder: str, genre: str, n_mels=128, n_mfcc=20, **kwargs
):
    """
    input_folder: folder which contains subfolder of genres
    output_folder: folder to store output numpy files
    genre: subfolder name inside input folder which contains audio files
    n_mels: number of bands (Mels) for (Mel-)Spectrogram extractor, default 128
    n_mfcc: number of MFCCs to return, default 20
    """


    genre_input_folder = f"{input_folder}/{genre}/"
    genre_output_folder = f"{output_folder}/{genre}/"

    # try and create
    try:
        os.makedirs(genre_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for file_name in list(os.listdir(genre_input_folder)):
        if os.path.isfile(f"{genre_input_folder}/{file_name}") and file_name.endswith(".wav"):
            LOGGER.info(f"extract_features.task >>> INFO current file: {file_name}")

            file_name_wo_ex = file_name[:-4]
            # load audio file
            y, sr = librosa.load(f"{genre_input_folder}/{file_name}")
            # Trim leading and trailing silence from an audio signal
            y, _ = librosa.effects.trim(y)

            # generate Mel Spectrogram
            S = librosa.feature.melspectrogram(y, sr=sr, n_mels=n_mels)
            np.save(f"{genre_output_folder}/{file_name_wo_ex}_melspectrogram.npy", S)

            # generate MFCCs
            mfccs = librosa.feature.mfcc(y, sr=sr, n_mfcc=n_mfcc)
            np.save(f"{genre_output_folder}/{file_name_wo_ex}_mfcc.npy", mfccs)
