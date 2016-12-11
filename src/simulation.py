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
        ImprovisingAgent(env, insp_set={'bach': 10, 'keith_jarrett': 10, 'motets': 5}, motif_length=3, memory_size=5,
                         name='Agent_' + str(i), pr_of_contrast=0.7, conf_decline_factor=0.8, conf_th=0.04)

#    ImprovisingAgent(env, insp_set={'bach': 0, 'keith_jarrett': 8, 'motets': 0}, motif_length=5, memory_size=10, name='Agent_0', pr_of_contrast=0.1)
#    ImprovisingAgent(env, insp_set={'bach': 0, 'keith_jarrett': 5, 'motets': 0}, motif_length=5, memory_size=10, name='Agent_1', pr_of_contrast=0.6)
#    ImprovisingAgent(env, insp_set={'bach': 8, 'keith_jarrett': 0, 'motets': 0}, motif_length=5, memory_size=10, name='Agent_2', pr_of_contrast=0.1)
#    ImprovisingAgent(env, insp_set={'bach': 5, 'keith_jarrett': 0, 'motets': 0}, motif_length=5, memory_size=10, name='Agent_3', pr_of_contrast=0.6)

    sim = creamas.Simulation(env, log_folder='logs', callback=env.agents_listen_and_evaluate)
    sim.async_steps(num_steps)
    sim.end()


if __name__ == "__main__":
    run_simulation(60, 6)