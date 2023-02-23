from ue5env import UE5EnvWrapper
from boxnavigator import Action, BoxNavigatorBase
from math import degrees
from box import Pt

# Defined in the Oldenborg Training Repository
from UE5datacollector import UE5DataCollection


class NavigatorUnrealWrapper:
    def __init__(
        self,
        navigator: BoxNavigatorBase,
        dataset_path: str,
        path_to_unreal_project_image: str,
        port: int = 8500,
        collect_data: bool = False,
    ) -> None:
        self.ue5 = UE5EnvWrapper(port)
        self.navigator = navigator
        self.collect_data = collect_data
        self.dataset_path = dataset_path
        self.path_to_unreal_project_image = path_to_unreal_project_image
        self.UE5_data_collector = UE5DataCollection(
            self.ue5, dataset_path, path_to_unreal_project_image
        )
        self.sync_unreal_position_to_box()
        self.sync_rotation()
        self.reset()

    def sync_unreal_position_to_box(self) -> None:
        """Move Unreal Agent to match Boxsim Agent X and Y values"""
        _, _, unrealZ = self.ue5.get_camera_location(0)
        self.ue5.setCameraLocation(
            self.navigator.position.x, self.navigator.position.y, unrealZ
        )

    def sync_box_position_to_unreal(self) -> None:
        """Move Boxsim agent to match Unreal Agent Position"""
        unrealX, unrealY, _ = self.ue5.get_camera_location(0)
        self.navigator.move(Pt(unrealX, unrealY))

    def sync_rotation(self) -> None:
        """Sync Unreal's agent location to box navigator."""
        # Conversion from Box to unreal location is (180 - boxYaw) = unrealYaw
        unrealYaw: float = degrees(self.navigator.rotation)
        self.ue5.set_camera_yaw(unrealYaw, 0)

    def take_action(self) -> None:
        """Performs the same action the box navigator performed but on the Unreal Agent.

        Args:
            action (Action): The action to perform.
            navigator (BoxNavigatorBase): The navigator performing the action.

        Raises:
            RuntimeError: If the action is not defined as Forward, Back, ROTATE_LEFT, or ROTATE_RIGHT.
        """
        action_taken, correct_action = self.navigator.take_action()
        if self.collect_data:
            self.UE5_data_collector.collect_data(correct_action)

        if action_taken == Action.FORWARD:
            self.ue5.forward(self.navigator.translation_increment)
        elif action_taken == Action.BACKWARD:
            self.ue5.back(self.navigator.translation_increment)
        elif action_taken == Action.ROTATE_LEFT:
            self.syncRotation()
        elif action_taken == Action.ROTATE_RIGHT:
            self.syncRotation()
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
