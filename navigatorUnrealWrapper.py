from ue5env import UE5EnvWrapper
from boxnavigator import BoxNavigatorBase
from box import Pt


class NavigatorUnrealWrapper:
    ue5: UE5EnvWrapper = None
    navigator: BoxNavigatorBase = None
    rotationOffset: int = 0

    def __init__(self, navigator: BoxNavigatorBase, port: int = 8500) -> None:
        self.ue5 = UE5EnvWrapper(port)
        self.navigator = navigator

        _, unrealYRot, _ = self.ue5.getCameraRotation()
        self.ue5.setCameraRotation()
        # self.rotationOffset = unrealYRot

    def syncPositions(self) -> None:
        unrealX, unrealY, unrealZ = self.ue5.getCameraLocation()
        self.navigator.move(Pt(unrealX, unrealY))

    # def
