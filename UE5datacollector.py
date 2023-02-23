# !/usr/bin/env python
import matplotlib.pyplot as plt

from ue5env import UE5EnvWrapper
import shutil
import random
import os
import time
import sys

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

    def collect_data(self, action: Action):
        # Generate unique file name, for now simply a float between 0 and 1 with the '0.' removed
        num = str(random.random())
        num = num.split(".")
        image_name = f"{num[1]}"
        try:
            os.mkdir(self.dataset_path)
        except OSError as error:
            pass
        try:
            if action == Action.FORWARD:
                self.env.save_image(0)
                shutil.move(
                    self.path_to_unreal_project_image,
                    f"{self.dataset_path}/forward_{image_name}.png",
                )
            elif action == Action.BACKWARD:
                self.env.save_image(0)
                shutil.move(
                    self.path_to_unreal_project_image,
                    f"{self.dataset_path}/backward{image_name}.png",
                )
            elif action == Action.ROTATE_LEFT:
                self.env.save_image(0)
                shutil.move(
                    self.path_to_unreal_project_image,
                    f"{self.dataset_path}/right_{image_name}.png",
                )
            elif action == Action.ROTATE_RIGHT:
                self.env.save_image(0)
                # Due to the inverted X axis, the rotate left action visually appears as a rotate right,
                # hence why the image annotation here shows "left"
                shutil.move(
                    self.path_to_unreal_project_image,
                    f"{self.dataset_path}/left_{image_name}.png",
                )
            else:
                return
        except:
            # in case shutil tries to move non existent file
            time.sleep(2)
            return
