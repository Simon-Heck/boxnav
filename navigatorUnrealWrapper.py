from ue5env import UE5EnvWrapper
import ue5env
from UE5_Data_collector import UE5_data_collection
from boxnavigator import Action, BoxNavigatorBase
from math import degrees, radians
from box import Box, Pt


class NavigatorUnrealWrapper:
    # ue5: UE5EnvWrapper = None
    # this is a wrapper

    def __init__(self, navigator: BoxNavigatorBase, port: int = 8500) -> None:
        self.experiment_name = "Test"
        self.ue5 = UE5EnvWrapper(port)
        self.navigator = navigator
        self.UE5_data_collector = UE5_data_collection(self.ue5, self.experiment_name)
        self.syncUnrealPositionToBox()
        self.syncRotation()

    def syncUnrealPositionToBox(self) -> None:
        """Move Unreal Agent to match Boxsim Agent X and Y values"""
        _, _, unrealZ = self.ue5.getCameraLocation(0)
        self.ue5.setCameraLocation(
            self.navigator.position.x, self.navigator.position.y, unrealZ
        )

    def syncBoxPositionToUnreal(self) -> None:
        """Move Boxsim agent to match Unreal Agent Position"""
        unrealX, unrealY, _ = self.ue5.getCameraLocation(0)
        self.navigator.move(Pt(unrealX, unrealY))

    def syncRotation(self) -> None:
        """Sync Unreal's agent location to box navigator."""
        # Conversion from Box to unreal location is (180 - boxYaw) = unrealYaw
        unrealYaw: float = degrees(self.navigator.rotation)
        self.ue5.setCameraYaw(unrealYaw, 0)

    def take_action(self) -> None:
        """Performs the same action the box navigator performed but on the Unreal Agent.

        Args:
            action (Action): The action to perform.
            navigator (BoxNavigatorBase): The navigator performing the action.

        Raises:
            RuntimeError: If the action is not defined as Forward, Back, ROTATE_LEFT, or ROTATE_RIGHT.
        """
        action_taken, correct_action = self.navigator.take_action()
        self.UE5_data_collector.collectData(correct_action)
        if action_taken == Action.FORWARD:
            self.ue5.forward(self.navigator.translation_increment)
        elif action_taken == Action.BACKWARD:
            self.ue5.back(self.navigator.translation_increment)
        elif action_taken == Action.ROTATE_LEFT:
            self.syncRotation()
            # self.ue5.left(degrees(navigator.rotation_increment))
        elif action_taken == Action.ROTATE_RIGHT:
            self.syncRotation()
            # self.ue5.right(degrees(navigator.rotation_increment))
        else:
            raise RuntimeError(
                f"Trying to perform an action that is undefined. Action# = {action_taken}"
            )
        return action_taken, correct_action

    def at_final_target(self):
        return self.navigator.at_final_target()

    def display(self, ax, scale):
        return self.navigator.display(ax, scale)

    def reset(self):
        return self.ue5.reset()
