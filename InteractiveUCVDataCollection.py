# !/usr/bin/env python
import matplotlib.pyplot as plt

from ue5env import UE5EnvWrapper
import shutil
import random

from ArcsLab.boxnav.boxnavigator import Action

# env = UE5EnvWrapper()
# fig, ax = plt.subplots()

# def main():

#     fig.canvas.mpl_connect("key_press_event", onpress)
#     plt.title("Unreal Engine View")
#     plt.axis("off")
#     ax.imshow(env.request_image(cameraNum=0))
#     plt.show()
def __init__(self, ue5env, batch_name):
    self.env = ue5env
    self.experiment_name = experiment_name
    # folder name ^^^^


def collectData(self, action: Action):
    path = "none"
    # Generate unique file name, for now simply a float between 0 and 1 with the '0.' removed
    num = str(random.random())
    num = num.split(".")
    imageName = f"{self.batch_name}-{num[1]}"

    datasetPath = "./Data/UE5Images"

    # if event.key == "w" or event.key == "up":
    #     path = self.env.save_image(0, f"{imageName}")
    #     shutil.move(path, f"{datasetPath}/forward")
    #     self.env.forward(30)

    # elif event.key == "a" or event.key == "left":
    #     path = self.env.save_image(0, f"{imageName}")
    #     shutil.move(path, f"{datasetPath}/left")
    #     self.env.left(30)

    # elif event.key == "d" or event.key == "right":
    #     path = self.env.save_image(0, f"{imageName}")
    #     shutil.move(path, f"{datasetPath}/right")
    #     self.env.right(30)
    # elif event.key == "s" or event.key == "down":
    #     path = self.env.save_image(0, f"{imageName}")
    #     shutil.move(path, f"{datasetPath}/back")
    #     self.env.back(30)
    # elif event.key == "backspace":
    #     self.env.reset()
    # else:
    #     return

    # ax.imshow(self.env.request_image(cameraNum=0))
    # fig.canvas.draw()
