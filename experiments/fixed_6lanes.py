import argparse
import os
import sys
from datetime import datetime

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

import traci
import sumo
from sumo_rl import SumoEnvironment
from sumo_rl.agents import QLAgent
from sumo_rl.exploration import EpsilonGreedy


if __name__ == '__main__':

    prs = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="""Q-Learning 6 lanes""")
    prs.add_argument("-route", dest="route", type=str, default='/home/longshui/ql-signal/nets/6lanes/single-intersection-heavy.rou.xml', help="Route definition xml file.\n")

    prs.add_argument("-mingreen", dest="min_green", type=int, default=10, required=False, help="Minimum green time.\n")
    prs.add_argument("-maxgreen", dest="max_green", type=int, default=30, required=False, help="Maximum green time.\n")
    prs.add_argument("-gui", action="store_true", default=False, help="Run with visualization on SUMO.\n")
    prs.add_argument("-fixed", action="store_true", default=True, help="Run with fixed timing traffic signals.\n")
    prs.add_argument("-s", dest="seconds", type=int, default=10000, required=False, help="Number of simulation seconds.\n")
    prs.add_argument("-runs", dest="runs", type=int, default=1, help="Number of runs.\n")
    args = prs.parse_args()
    experiment_time = str(datetime.now()).split('.')[0]
    out_csv = '../outputs/fixed_6lanes/fixed_heavy'

    env = SumoEnvironment(net_file='//nets/6lanes/single-Intersection.net.xml',
                          route_file=args.route,
                          out_csv_name=out_csv,
                          use_gui=args.gui,
                          num_seconds=args.seconds,  #simulation time
                          min_green=args.min_green,
                          max_green=args.max_green,
                          max_depart_delay=0)

    for run in range(1, args.runs+1):
        initial_states = env.reset()
        done = {'__all__': False}
        infos = []
        if args.fixed:
            seconds = 0
            while not done['__all__']:
                _, _, done, _ = env.step_long(None, seconds)
                seconds += 1
        else:
            pass
        env.save_csv(out_csv, run)

        env.close()