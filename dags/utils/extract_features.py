import os, errno
from typing import Any

import librosa
import numpy as np
import os
import logging

LOGGER = logging.getLogger(__name__)


def extract_features(
    input_folder: str, output_folder: str, n_mels=128, n_mfcc=20, **kwargs
):
    """
    input_folder: folder which contains subfolder of genres
    output_folder: folder to store output numpy files
    n_mels: number of bands (Mels) for (Mel-)Spectrogram extractor, default 128
    n_mfcc: number of MFCCs to return, default 20
    """

    for genre in list(os.listdir(input_folder)):
        if os.path.isdir(f"{input_folder}/{genre}"):
            genre_input_folder = f"{input_folder}/{genre}/"
            genre_output_folder = f"{output_folder}/{genre}/"

            LOGGER.info(
                f"extract_features.task >>> INFO current folder: {genre_input_folder}"
            )

            # try and create output folder
            try:
                os.makedirs(genre_output_folder)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            for file_name in list(os.listdir(genre_input_folder)):
                input_file_abs_path = f"{genre_input_folder}/{file_name}"
                if os.path.isfile(input_file_abs_path) and file_name.endswith(".wav"):
                    LOGGER.info(
                        f"extract_features.task >>> INFO current file: {input_file_abs_path}"
                    )

                    file_name_wo_ex = file_name[:-4]
                    # load audio file and trim leading and trailing silence from an audio signal
                    y, sr = librosa.load(f"{input_file_abs_path}")
                    y, _ = librosa.effects.trim(y)

                    # generate Mel Spectrogram
                    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=n_mels)
                    np.save(
                        f"{genre_output_folder}/{file_name_wo_ex}_melspectrogram.npy", S
                    )

                    # generate MFCCs
                    mfccs = librosa.feature.mfcc(y, sr=sr, n_mfcc=n_mfcc)
                    np.save(f"{genre_output_folder}/{file_name_wo_ex}_mfcc.npy", mfccs)
