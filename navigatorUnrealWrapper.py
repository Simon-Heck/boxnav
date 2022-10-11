from ue5env import UE5EnvWrapper
from boxnavigator import Action, BoxNavigatorBase
from math import degrees, radians
from box import Box, Pt


class NavigatorUnrealWrapper:
    ue5: UE5EnvWrapper = None

    def __init__(self, navigator: BoxNavigatorBase, port: int = 8500) -> None:
        self.ue5 = UE5EnvWrapper(port)
        self.navigator = navigator
        self.syncUnrealPositionToBox(navigator)
        self.syncRotation(navigator)

    def syncUnrealPositionToBox(self, navigator: BoxNavigatorBase) -> None:
        """Move Unreal Agent to match Boxsim Agent X and Y values"""
        _, _, unrealZ = self.ue5.getCameraLocation(0)
        self.ue5.setCameraLocation(navigator.position.x, navigator.position.y, unrealZ)

    def syncBoxPositionToUnreal(self, navigator: BoxNavigatorBase) -> None:
        """Move Boxsim agent to match Unreal Agent Position"""
        unrealX, unrealY, _ = self.ue5.getCameraLocation(0)
        navigator.move(Pt(unrealX, unrealY))

    def syncRotation(self, navigator: BoxNavigatorBase) -> None:
        """Sync Unreal's agent location to box navigator."""
        # Conversion from Box to unreal location is (180 - boxYaw) = unrealYaw
        unrealYaw: float = 180 - degrees(navigator.rotation)
        self.ue5.setCameraYaw(unrealYaw, 0)

    def takeAction(self, action: Action, navigator: BoxNavigatorBase) -> None:
        """Performs the same action the box navigator performed but on the Unreal Agent.

        Args:
            action (Action): The action to perform.
            navigator (BoxNavigatorBase): The navigator performing the action.

        Raises:
            RuntimeError: If the action is not defined as Forward, Back, ROTATE_LEFT, or ROTATE_RIGHT.
        """
        if action == Action.FORWARD:
            self.ue5.forward(navigator.translation_increment)
        elif action == Action.BACKWARD:
            self.ue5.back(navigator.translation_increment)
        elif action == Action.ROTATE_LEFT:
            self.ue5.left(degrees(navigator.rotation_increment))
        elif action == Action.ROTATE_RIGHT:
            self.ue5.right(degrees(navigator.rotation_increment))
        else:
            raise RuntimeError(
                f"Trying to perform an action that is undefined. Action# = {action}"
            )
