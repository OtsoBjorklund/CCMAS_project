# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#

from datetime import datetime

import musicxmlio
from creamas import Environment

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
        musicxmlio.parts_to_musicxml(self.parts, filename)

    def save_info(self, folder, *args, **kwargs):
        folder = 'output'
        timestamp = '{:%Y%m%d_%H%M%S}'.format(datetime.now())
        # form = 20161203_162901
        filename = 'Improvisation_' + timestamp + '.xml'
        path = folder + '/' + filename
        self.save_improvisation(path)

    def play_music(self, age):
        pass
