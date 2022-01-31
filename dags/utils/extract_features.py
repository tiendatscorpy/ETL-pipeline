import os, errno
from typing import Any, Dict
import librosa
import numpy as np
import json
import logging

LOGGER = logging.getLogger(__name__)


def extract_features(input_folder: str, output_folder: str, op_conf: str, **kwargs):
    """
    input_folder: folder which contains subfolder of genres
    output_folder: folder to store output numpy files
    n_mels: number of bands (Mels) for (Mel-)Spectrogram extractor, default 128
    n_mfcc: number of MFCCs to return, default 20
    n_fft: length of the FFT window, default 2048
    hop_length: number of samples between successive frames, default 512
    win_length: Each frame of audio is windowed by window(). The window will be of length win_length and then padded with zeros to match n_fft. If unspecified, defaults to win_length = n_fft
    dct_type: Discrete cosine transform (DCT) type. By default, 2
    """

    optional_params = eval(op_conf)
    n_mels = optional_params.get("n_mels", 128)
    n_mfcc = optional_params.get("n_mfcc", 20)
    n_fft = optional_params.get("n_fft", 2048)
    hop_length = optional_params.get("hop_length", 512)
    win_length = optional_params.get("win_length", n_fft)
    dct_type = optional_params.get("dct_type", 2)

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
                    S = librosa.feature.melspectrogram(
                        y,
                        sr=sr,
                        n_mels=n_mels,
                        hop_length=hop_length,
                        win_length=win_length,
                    )
                    np.save(
                        f"{genre_output_folder}/{file_name_wo_ex}_melspectrogram.npy", S
                    )

                    # generate MFCCs
                    mfccs = librosa.feature.mfcc(
                        y, sr=sr, n_mfcc=n_mfcc, dct_type=dct_type
                    )
                    np.save(f"{genre_output_folder}/{file_name_wo_ex}_mfcc.npy", mfccs)
