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
        # folder name ^^^^

    def collectData(self, action: Action):
        path = "none"
        # Generate unique file name, for now simply a float between 0 and 1 with the '0.' removed
        num = str(random.random())
        num = num.split(".")
        imageName = f"{num[1]}"
        datasetPath = f"./Data/UE5Images/{self.experiment_name}"
        try:
            os.mkdir(datasetPath)
        except OSError as error:
            print(error)

        if action == Action.FORWARD:
            path = self.env.save_image(0, "", f"{imageName}")
            shutil.move(path, f"{datasetPath}")
        elif action == Action.BACKWARD:
            path = self.env.save_image(0, "", f"{imageName}")
            shutil.move(path, f"{datasetPath}")
        elif action == Action.ROTATE_LEFT:
            path = self.env.save_image(0, "", f"{imageName}")
            shutil.move(path, f"{datasetPath}")
        elif action == Action.ROTATE_RIGHT:
            path = self.env.save_image(0, ".jpg", f"{imageName}")
            shutil.move(path, f"{datasetPath}")
        else:
            return
