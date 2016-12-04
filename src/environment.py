# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#

from datetime import datetime

import musicxmlio
from creamas import Environment, Artifact


class MusicEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = {}

    def add_music_to_part(self, part_name, motif):
        """ Add motif to the parts """
        if part_name not in self._parts:
            self._parts[part_name] = []

        self._parts[part_name].append(motif)

    def save_improvisation(self, filename):
        """ Save the improvisation to file """
        musicxmlio.parts_to_musicxml(self._parts, filename)

    def save_info(self, folder, *args, **kwargs):
        folder = 'output'
        timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
        # form = 20161203_162901
        filename = 'Improvisation_' + timestamp + '.xml'
        path = folder + '/' + filename
        self.save_improvisation(path)

    def get_musical_context(self, age):
        context = []

        for part in self._parts:
            lower_index = max(0, len(self._parts[part]) - 5)
            for i in range(lower_index, age):
                context.append(self._parts[part][i])

        return context

    def agents_listen_and_evaluate(self, age):
        context = self.get_musical_context(age)
        for agent in self.get_agents(address=False):
            agent.listen_to_others(context)
            motif = Artifact(agent, self._parts[agent.name][age - 1], domain='music')
            agent.evaluate(motif)

