# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#
# This is the file to execute if you want to run the simulation.

import creamas
from environment import MusicEnvironment

from impro_agent import ImprovisingAgent


def run_simulation(num_steps, num_agents):
    """ Runs the simulation.
        :param num_steps: Number of steps to run in simulation.
        :type num_steps: int
        :param num_agents: Number of agents to use in simulation.
        :type num_agents: int """

    env = MusicEnvironment.create(('localhost', 5555))
    for i in range(0, num_agents):
        agent = ImprovisingAgent(env, insp_set={'bach': 0, 'keith_jarrett': 0, 'motets': 2}, motif_length=2, memory_size=3, name='Agent_' + str(i))

    sim = creamas.Simulation(env, log_folder='logs', callback=env.agents_listen_and_evaluate)
    sim.async_steps(num_steps)
    sim.end()


if __name__ == "__main__":
    run_simulation(50, 10)