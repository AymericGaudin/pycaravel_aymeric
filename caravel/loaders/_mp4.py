##########################################################################
# NSAp - Copyright (C) CEA, 2020
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module defines the mp4 dataset loader.
"""

# Imports
import subprocess

# Third party import
import imageio

# Package import
from .loader_base import LoaderBase


def is_mp4(path, verbose=False):
    """Check if a file is truly a mp4 file by checking its actual content.
    It uses the 'file' command line to do so.

    Parameters
    ----------
    path: str
        Path to the file to be checked.
    verbose: bool, default False
        Whether to print or not the 'file' command output.
    """
    cmd = ["file", path]
    output = subprocess.check_output(cmd).decode()
    if verbose: print(output)
    output = output.strip(path)
    output = output.lower()
    return "mp4" in output


class MP4(LoaderBase):
    """ Define the mp4 loader.
    """
    allowed_extensions = [".mp4"]

    def load(self, path):
        """ A method that load the mp4 data.

        Parameters
        ----------
        path: str
            the path to the mp4 file to be loaded.

        Returns
        -------
        data: imageio numpy array
            the loaded image.
        """
        assert is_mp4(path, verbose=False), f"{path} is not a mp4 file"
        return imageio.get_reader(path,  'ffmpeg')

    def save(self, data, outpath, fps=24):
        """ A method that save the image in mp4.

        Parameters
        ----------
        data: list of path
            list of path for each image for the video.
        outpath: str
            the path where the the mp4 image will be saved.
        """

        writer = imageio.get_writer(outpath, fps)
        for png_path in data:
            im = imageio.imread(png_path),
            writer.append_data(im[:, :, 1])
        writer.close()
