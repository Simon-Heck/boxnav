import math
from boxunrealwrapper import NavigatorUnrealWrapper
from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator, WanderingNavigator, Action
from celluloid import Camera
import matplotlib.pyplot as plt
from argparse import ArgumentParser

# boxes = [
#     # Box(Pt(-190, -350), Pt(-190, 1070), Pt(420, 1070), Pt(115, 1020)),
#     # Box(Pt(-365, 600), Pt(-450, 600), Pt(-190, 240), Pt(-700, 240)),
#     # Box(Pt(480, -2550), Pt(480, 3070), Pt(-6520, 3070), Pt(0, 0)),
#     Box(Pt(-185, 1060), Pt(420, 1060), Pt(420, -350), Pt(10, 420)),
#     Box(Pt(-1110, 590), Pt(420, 590), Pt(420, 245), Pt(-770, 420)),
#     Box(Pt(-855, -100), Pt(-855, 590), Pt(-700, 590), Pt(-780, 0)),
#     Box(Pt(-700, 65), Pt(-700, -100), Pt(-4690, -100), Pt(-4500, -32)),
#     Box(Pt(-4690, 65), Pt(-4415, 65), Pt(-4415, -2400), Pt(-4580, -2245)),
#     Box(Pt(-4415, -2090), Pt(-4415, -2400), Pt(-5755, -2400), Pt(-5575, -2220)),
#     Box(Pt(-5530, -2400), Pt(-5755, -2400), Pt(-5755, 2845), Pt(-5655, 1983)),
#     # Box(Pt(-5755, 1680), Pt(-5755, -2350), Pt(-4600, 2350), Pt(-5000, 1983)),
# ]

# route 2, uses path w/ waterfountain & stairs
boxes = [
    Box(Pt(-185, 1060), Pt(420, 1060), Pt(420, -350), Pt(10, 420)),
    Box(Pt(-1110, 590), Pt(420, 590), Pt(420, 245), Pt(-770, 420)),
    Box(Pt(-855, -100), Pt(-855, 590), Pt(-700, 590), Pt(-780, 0)),
    Box(Pt(-700, 65), Pt(-700, -100), Pt(-4690, -100), Pt(-4500, -32)),
    Box(Pt(-4690, 65), Pt(-4415, 65), Pt(-4415, -2400), Pt(-4570, -433)),
    Box(Pt(-4415, -295), Pt(-4415, -640), Pt(-5755, -640), Pt(-5590, -450)),
    Box(Pt(-5530, -2400), Pt(-5755, -2400), Pt(-5755, 2845), Pt(-5655, 1983)),
    # Box(Pt(-5755, 1680), Pt(-5755, -2350), Pt(-4600, 2350), Pt(-5000, 1983)),
]


def simulate():
    """Create and update the box environment and run the navigator."""
    path_to_dataset = "C:/Users/simon/OneDrive/Documents/ArcsLab/ArcLabPrograms/UE5Images/small_test_folder"
    path_to_unreal_project_image = "C:/Users/simon/OneDrive/Documents/Unreal Projects/OldenborgUE/Saved/Screenshots/WindowsEditor/highres.png"
    env = BoxEnv(boxes)

    agent_position = Pt(0, 0)
    agent_rotation = math.radians(90)
    # 180 minus script rotation is unreal rotation

    if args.navigator == "wandering":
        agent = WanderingNavigator(
            agent_position,
            agent_rotation,
            env,
            out_of_bounds=args.ue,
            chance_of_random_action=0.25,
        )
    elif args.navigator == "perfect":
        agent = PerfectNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue
        )
    else:
        raise ValueError("Invalid argument error (check code for options).")

    if args.ue:
        agent = NavigatorUnrealWrapper(
            agent,
            path_to_dataset,
            path_to_unreal_project_image,
            port=8500,
            collect_data=args.collect,
        )
        agent.reset()

    fig, ax = plt.subplots()
    camera = Camera(fig)

    # TODO: turn into CLI argument
    max_actions_to_take = 5
    num_actions_taken = 0
    while not agent.at_final_target():
        # TODO: some kind of corrective action?
        action_taken, correct_action = agent.take_action()

        # if action_taken == Action.FORWARD:
        #     ue5.forward(agent.translation_increment)
        # else:
        #     raise NotImplemented

        # agent.update_position()

        # TODO: use "correct_action" to label the image

        env.display(ax)
        agent.display(ax, env.scale)
        ax.invert_xaxis()
        camera.snap()

        num_actions_taken += 1
        if num_actions_taken >= max_actions_to_take:
            break

    print(
        f"Simulation complete, it took {num_actions_taken} actions to reach the end. Now creating output."
    )

    anim = camera.animate()
    anim.save("output." + args.save_ext)  # type: ignore


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
argparser.add_argument(
    "--navigator", type=str, default="wandering", help="Navigator to use."
)
argparser.add_argument(
    "--ue", action="store_true", help="Navigate in Unreal Engine environment."
)
argparser.add_argument(
    "--collect",
    action="store_true",
    help="Collect data while navigating",
    default="store_false",
)
args = argparser.parse_args()
simulate()
