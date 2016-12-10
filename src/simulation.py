import creamas
from environment import MusicEnvironment

from impro_agent import ImprovisingAgent


def run_simulation(num_steps, num_agents):
    env = MusicEnvironment.create(('localhost', 5555))
    for i in range(0, num_agents):
        agent = ImprovisingAgent(env, insp_set= {'keith_jarrett':1}, motif_length=2, memory_size=5, name='Agent_' + str(i))

    sim = creamas.Simulation(env, log_folder='logs', callback=env.agents_listen_and_evaluate)
    sim.async_steps(num_steps)
    sim.end()


if __name__ == "__main__":
    run_simulation(30, 2)