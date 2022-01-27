import os, errno
import numpy as np
import os
from sklearn.preprocessing import scale, minmax_scale
import logging

LOGGER = logging.getLogger(__name__)

def scale_features(
    input_folder: str,
    output_folder: str,
    genre: str,
    **kwargs):
    """
    input_folder: folder which contains input audio files
    output_folder: folder to store output numpy files
    num_bands: number of bands (Mels) for (Mel-)Spectrogram extractor
    """
    genre_input_folder = f'{input_folder}/{genre}/'
    genre_output_folder = f'{output_folder}/{genre}/'

    try:
        os.makedirs(genre_output_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    for file_name in list(os.listdir(genre_input_folder)):
        if os.path.isfile(f"{genre_input_folder}/{file_name}") and file_name.endswith(".npy"):
            LOGGER.info(f"scale_features.task >>> INFO current file: {file_name}")

            file_name_wo_ex = file_name[:-4]

            # load np array
            y = np.load(f'{genre_input_folder}/{file_name}')

            y_std_scaled = scale(y)
            np.save(f'{genre_output_folder}/{file_name_wo_ex}_standardcaler.npy',y_std_scaled)

            y_mm_scaled = minmax_scale(y)
            np.save(f'{genre_output_folder}/{file_name_wo_ex}_minmaxnormalizer.npy',y_mm_scaled)

