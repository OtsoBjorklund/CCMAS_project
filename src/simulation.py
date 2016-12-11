# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#
# This is the file to execute if you want to run the simulation.

import creamas
from environment import MusicEnvironment

from impro_agent import ImprovisingAgent


def create_agents(env):
    """ Create a number of agents for the simulation. If you want to try out different things, modify this. """
    ImprovisingAgent(env, insp_set={'bach': 8, 'keith_jarrett': 6, 'motets': 1}, motif_length=2, memory_size=8,
                     name='Agent_0', pr_of_contrast=0.3, conf_decline_factor=0.8, conf_th=0.001)
    ImprovisingAgent(env, insp_set={'bach': 8, 'keith_jarrett': 2, 'motets': 4}, motif_length=2, memory_size=8,
                     name='Agent_1', pr_of_contrast=0.3, conf_decline_factor=0.8, conf_th=0.01)
    ImprovisingAgent(env, insp_set={'bach': 8, 'keith_jarrett': 6, 'motets': 1}, motif_length=2, memory_size=8,
                     name='Agent_2', pr_of_contrast=0.3, conf_decline_factor=0.8, conf_th=0.1)
    ImprovisingAgent(env, insp_set={'bach': 8, 'keith_jarrett': 2, 'motets': 4}, motif_length=2, memory_size=8,
                     name='Agent_3', pr_of_contrast=0.3, conf_decline_factor=0.8, conf_th=0.05)


def run_simulation(num_steps):
    """ Runs the simulation.

        :param num_steps: Number of steps to run in simulation.
        :type num_steps: int """

    env = MusicEnvironment.create(('localhost', 5555))
    create_agents(env)
    sim = creamas.Simulation(env, log_folder='logs', callback=env.agents_listen_and_evaluate)
    sim.async_steps(num_steps)
    sim.end()


if __name__ == "__main__":
    run_simulation(70)
