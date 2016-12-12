# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#

from datetime import datetime

import musicxmlio
import os
from creamas import Environment, Artifact
from math import ceil


class MusicEnvironment(Environment):
    """ The environment that the agents play in.
        Keeps track of everything that the agents have played and outputs it at the end into a MusicXML file. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = {}
        self._max_agent_memory_cap = None

    def add_music_to_part(self, part_name, motif):
        """ Add motif to the parts.

            :param part_name: Name of the part that the motif is added to.
            :type part_name: str
            :param motif: The motif that is added to part.
            :type motif: Motif """

        if part_name not in self._parts:
            self._parts[part_name] = []

        self._parts[part_name].append(motif)

    def save_improvisation(self, filename):
        """ Save the improvisation to MusicXML file.

            :param filename: The name of the output file.
            :type filename: str """

        musicxmlio.parts_to_musicxml_midi(self._parts, filename)

    def save_info(self, folder, *args, **kwargs):
        """ When the environment is destroyed this is called.
            Save the results of the simulation, i.e. the improvisation into file. """

        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
        # form = 20161203_162901
        filename = 'Improvisation_' + timestamp
        path = output_dir + '/' + filename
        self.save_improvisation(path)

    @property
    def max_agent_memory_capacity(self):
        """ The largest memory capacity of any agent in the environment. """

        # Agents cannot leave or enter the environment, so this needs to be computed only once
        if self._max_agent_memory_cap is None:
            max_mem_size = 0
            for agent in self.get_agents(address=False):
                mem_size = agent.memory_capacity
                if mem_size > max_mem_size:
                    max_mem_size = mem_size

            self._max_agent_memory_cap = max_mem_size

        return self._max_agent_memory_cap

    def get_latest_motifs(self, age):
        """ Get all the motifs that have been played recently. Get only slightly more motifs
            than can be remembered by the agent with maximum memory size.

            :param age: The current number of simulation step.
            :type age: int
            :return: List of Motifs.
            :rtype: list """

        latest_motifs = []
        distance = ceil(self.max_agent_memory_capacity / len(self.get_agents(address=False)))

        for part in self._parts:
            lower_index = max(0, len(self._parts[part]) - distance)
            for i in range(lower_index, age):
                latest_motifs.append(self._parts[part][i])

        return latest_motifs

    def agents_listen_and_evaluate(self, age):
        """ Agents listen to what has been played in the environment
            and evaluate their own performance in regard to that.

            :param age: The step of the simulation.
            :type age: int """

        latest_motifs = self.get_latest_motifs(age)
        for agent in self.get_agents(address=False):
            agent.listen_to_others(latest_motifs, age)
            motif = Artifact(agent, self._parts[agent.name][age - 1], domain='music')
            agent.evaluate(motif)

