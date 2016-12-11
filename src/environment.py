# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#

from datetime import datetime

import musicxmlio
import os
from creamas import Environment, Artifact


class MusicEnvironment(Environment):
    """ The environment that the agents play in.
        Keeps track of everything that the agents have played and outputs it at the end into a MusicXML file. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = {}

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

        musicxmlio.parts_to_musicxml(self._parts, filename)

    def save_info(self, folder, *args, **kwargs):
        """ When the environment is destroyed this is called.
            Save the results of the simulation, i.e. the improvisation into file. """

        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
        # form = 20161203_162901
        filename = 'Improvisation_' + timestamp + '.xml'
        path = output_dir + '/' + filename
        self.save_improvisation(path)

    def get_musical_context(self, age, distance=3):
        """ Get all the motifs that all agents have played before age and after distance.

            :param age: The current number of simulation step.
            :type age: int
            :param distance: How many steps back should be considered.
            :type distance: int
            :return: List of Motifs.
            :rtype: list """

        context = []

        for part in self._parts:
            lower_index = max(0, len(self._parts[part]) - distance)
            for i in range(lower_index, age):
                context.append(self._parts[part][i])

        return context

    def agents_listen_and_evaluate(self, age):
        """ Agents listen to what has been played in the environment
            and evaluate their own performance in regard to that. """

        context = self.get_musical_context(age)
        for agent in self.get_agents(address=False):
            agent.listen_to_others(context)
            motif = Artifact(agent, self._parts[agent.name][age - 1], domain='music')
            agent.evaluate(motif)

