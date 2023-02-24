# !/usr/bin/env python

from ue5env import UE5EnvWrapper
import shutil
import random
import os
import time

from boxnavigator import Action


class UE5DataCollection:
    def __init__(
        self,
        ue5env: UE5EnvWrapper,
        dataset_path: str,
        path_to_unreal_project_image: str,
    ):
        self.env = ue5env
        self.dataset_path = dataset_path
        # Path to location UE5 stores high res photos(includes name of the photo, which is modified in blueprints)
        self.path_to_unreal_project_image = path_to_unreal_project_image
