import math
from navigatorUnrealWrapper import NavigatorUnrealWrapper
from box import Box, Pt
from boxenv import BoxEnv
from boxnavigator import PerfectNavigator, WanderingNavigator, Action

# from ue5env import UE5Wrapper

from celluloid import Camera
import matplotlib.pyplot as plt

from argparse import ArgumentParser


# TODO: update to reflect OldenborgUE
boxes = [
    # Box(Pt(-190, -350), Pt(-190, 1070), Pt(420, 1070), Pt(115, 1020)),
    # Box(Pt(-365, 600), Pt(-450, 600), Pt(-190, 240), Pt(-700, 240)),
    
    # Box(Pt(480, -2550), Pt(480, 3070), Pt(-6520, 3070), Pt(0, 0)),
    Box(Pt(-185, 1060), Pt(420, 1060), Pt(420, -350), Pt(10, 420)),
    Box(Pt(-1110, 590), Pt(420, 590), Pt(420, 245), Pt(-770, 420)),
]


def simulate():
    """Create and update the box environment and run the navigator."""
    env = BoxEnv(boxes)

    agent_position = Pt(0, 0)
    agent_rotation = math.radians(90)
    # 180 minus script rotation is unreal rotation

    if args.navigator == "wandering":
        agent = WanderingNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue
        )
    elif args.navigator == "perfect":
        agent = PerfectNavigator(
            agent_position, agent_rotation, env, out_of_bounds=args.ue
        )
    else:
        raise ValueError("Invalid argument error (check code for options).")

    if args.ue:
        agent = NavigatorUnrealWrapper(agent, 8500)
    # else:
    #     navUnrealWrapper = None
    
    fig, ax = plt.subplots()
    camera = Camera(fig)

    # TODO: turn into CLI argument
    max_actions_to_take = 25
    num_actions_taken = 0

    while not agent.at_final_target():

        # if navUnrealWrapper is not None:
        # if agent.isOutOfBounds:
        #     navUnrealWrapper.syncBoxPositionToUnreal(agent)
        # else:
        #     navUnrealWrapper.syncUnrealPositionToBox(agent)
        # TODO Some kind of corrective action?
        # action_taken, correct_action = agent.take_action()
        action_taken, correct_action = agent.take_action()
        # Sync position in case Unreal Agent hits a wall and cannot move

        env.display(ax)
        agent.display(ax, env.scale)

        if num_actions_taken % 10 = 0:
            camera.snap()
            
        num_actions_taken += 1
        if num_actions_taken >= max_actions_to_take:
            break

    print(
        f"Simulation complete, it took {num_actions_taken} actions to reach the end. Now creating output."
    )
    
    anim = camera.animate()
    anim.save("output." + args.save_ext)


argparser = ArgumentParser("Navigate around a box environment.")
argparser.add_argument("save_ext", type=str, help="Extension for output format.")
argparser.add_argument(
    "--navigator", type=str, default="perfect", help="Navigator to use."
)
argparser.add_argument(
    "--ue", action="store_true", help="Navigate in Unreal Engine environment."
)
args = argparser.parse_args()

simulate()
