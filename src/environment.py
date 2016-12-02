# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#

from creamas import Environment
from datetime import datetime
import impro_agent
import musicxmlio


class MusicEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parts = {}

    def add_music_to_part(self, part_name, notes):
        """ Add notes to the parts """
        if part_name not in self.parts:
            self.parts[part_name] = []

        for note in notes:
            self.parts[part_name].append(note)

    def save_improvisation(self, filename):
        """ Save the improvisation to file """
        musicxmlio.parts_dictionary_to_musicxml(self.parts, filename)

    def save_info(self, folder, *args, **kwargs):
        folder = 'output'
        timestamp = str(datetime.now())
        filename = 'Improvisation_' + timestamp + '.xml'
        path = folder + '/' + filename
        self.save_improvisation(path)

    def play_music(self, age):
        for agent in self.get_agents(address=False):
            self.add_music_to_part(agent.name, agent.play_sequence())
