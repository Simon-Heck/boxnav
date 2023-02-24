from ue5env import UE5EnvWrapper
from boxnavigator import Action, BoxNavigatorBase
from math import degrees

# Defined in the Oldenborg Training Repository
from UE5datacollector import UE5DataCollection


class UENavigatorWrapper:
    """A wrapper for navigators that facilitates coordination with UnrealEngine 5."""

    def __init__(
        self,
        navigator: BoxNavigatorBase,
        dataset_path: str,
        ue_image_path: str,
        port: int = 8500,
        collect_data: bool = False,
    ) -> None:
        self.ue5 = UE5EnvWrapper(port)

        self.navigator = navigator
        self.dataset_path = dataset_path
        self.ue_image_path = ue_image_path
        self.collect_data = collect_data

        self.image_collector = UE5DataCollection(self.ue5, dataset_path, ue_image_path)

        # Sync UE and boxsim
        self.sync_positions()
        self.sync_rotation()
        self.reset()

    def at_final_target(self):
        return self.navigator.at_final_target()

    def display(self, ax, scale):
        return self.navigator.display(ax, scale)

    def reset(self):
        return self.ue5.reset()

    def sync_positions(self) -> None:
        """Move UE agent to match boxsim agent."""

        # Get z position from UE
        _, _, unreal_z = self.ue5.get_camera_location(0)

        # Get x, y position from boxsim
        x, y = self.navigator.position.xy()

        self.ue5.set_camera_location(x, y, unreal_z)

    # def sync_box_position_to_unreal(self) -> None:
    #     """Move Boxsim agent to match Unreal Agent Position"""
    #     unrealX, unrealY, _ = self.ue5.get_camera_location(0)
    #     self.navigator.move(Pt(unrealX, unrealY))

    def sync_rotation(self) -> None:
        """Sync UE agent location to box agent."""
        # Conversion from Box to unreal location is (180 - boxYaw) = unrealYaw
        unreal_yaw: float = degrees(self.navigator.rotation)
        self.ue5.set_camera_yaw(unreal_yaw, 0)

    def take_action(self) -> tuple[Action, Action]:
        """Execute action in the navigator and in the UE agent.

        Returns:
            tuple[Action, Action]: return action taken and correct action.

        Raises:
            RuntimeError: If the action is not defined.
        """

        action_taken, correct_action = self.navigator.take_action()
        if self.collect_data:
            self.image_collector.collect_data(correct_action)

        if action_taken == Action.FORWARD:
            self.ue5.forward(self.navigator.translation_increment)
        elif action_taken == Action.BACKWARD:
            self.ue5.back(self.navigator.translation_increment)
        elif action_taken == Action.ROTATE_LEFT:
            self.sync_rotation()
        elif action_taken == Action.ROTATE_RIGHT:
            self.sync_rotation()
        else:
            raise RuntimeError(f"Undefined action: {action_taken}")

        return action_taken, correct_action

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
