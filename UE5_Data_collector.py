# !/usr/bin/env python
import matplotlib.pyplot as plt

from ue5env import UE5EnvWrapper
import shutil
import random
import os

from boxnavigator import Action


class UE5_data_collection:
    def __init__(self, ue5env: UE5EnvWrapper, experiment_name: str):
        self.env = ue5env
        self.experiment_name = experiment_name
        self.image_extension = ".jpg"
        # folder name ^^^^

    def collectData(self, action: Action):
        # Generate unique file name, for now simply a float between 0 and 1 with the '0.' removed
        num = str(random.random())
        num = num.split(".")
        imageName = f"{num[1]}"
        datasetPath = f"C:\Users\simon\OneDrive\Documents\ArcsLab\ArcLabPrograms\UE5Images\1stRun"
        try:
            os.mkdir(datasetPath)
        except OSError as error:
            print(error)

        if action == Action.FORWARD:
            self.path = self.env.save_image(0, self.image_extension)
            shutil.move(
                self.path, f"{datasetPath}/forward_{imageName}{self.image_extension}"
            )
        elif action == Action.BACKWARD:
            self.path = self.env.save_image(0, self.image_extension)
            shutil.move(
                self.path, f"{datasetPath}/backward{imageName}{self.image_extension}"
            )
        elif action == Action.ROTATE_LEFT:
            self.path = self.env.save_image(0, self.image_extension)
            shutil.move(
                self.path, f"{datasetPath}/left_{imageName}{self.image_extension}"
            )
        elif action == Action.ROTATE_RIGHT:
            self.path = self.env.save_image(0, self.image_extension)
            shutil.move(
                self.path, f"{datasetPath}/right_{imageName}{self.image_extension}"
            )
        else:
            return
