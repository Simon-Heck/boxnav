from ue5env import UE5EnvWrapper
from boxnavigator import BoxNavigatorBase
from math import degrees, radians
from box import Box, Pt


class NavigatorUnrealWrapper:
    ue5: UE5EnvWrapper = None
    # navigator: BoxNavigatorBase = None

    def __init__(self, navigator: BoxNavigatorBase, port: int = 8500) -> None:
        self.ue5 = UE5EnvWrapper(port)
        self.navigator = navigator
        self.syncPositions(navigator)
        self.syncRotation(navigator)

    def syncPositions(self, navigator: BoxNavigatorBase) -> None:
        unrealX, unrealY, unrealZ = self.ue5.getCameraLocation(0)
        navigator.move(Pt(unrealX, unrealY))

    def syncRotation(self, navigator: BoxNavigatorBase) -> None:
        """Sync Unreal's agent location to box navigator."""
        # Conversion from Box to unreal location is (180 - boxYaw) = unrealYaw
        unrealYaw: float = 180 - degrees(navigator.rotation)
        self.ue5.setCameraYaw(unrealYaw, 0)
