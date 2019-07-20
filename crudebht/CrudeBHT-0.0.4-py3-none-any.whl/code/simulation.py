import argparse
from rendering import *
from os import path, mkdir

if not path.exists("./renders"):
    mkdir("./renders")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simulate N-Body Problem')
    parser.add_argument("simulation_type", help="BruteForce or BarnesHut")
    parser.add_argument("bodies", help="The number of bodies to simulate")
    parser.add_argument("frames", help="The number of frames to simulate for")
    parser.add_argument("trail_size", help="Display a trail of diameter x while rendering")
    parser.add_argument("--performance_test", help="don't render anything, just calculate", action="store_true")
    args = parser.parse_args()

    system = None
    if args.simulation_type == 'BarnesHut':
        system = RenderableBarnesHutSystem()
    elif args.simulation_type == 'BruteForce':
        system = RenderableBruteForceSystem()
    else:
        exit(1)

    system.start_the_bodies(int(args.bodies))
    renderer = SystemRenderer(system, frames=int(args.frames), trail_size=int(args.trail_size), performance_test=args.performance_test)

    renderer.run()