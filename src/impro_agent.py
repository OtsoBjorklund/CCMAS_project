# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random

from creamas import CreativeAgent
from motif import Motif

from src import musicxmlio


class ImprovisingAgent(CreativeAgent):

    def __init__(self, env, filename, motif_length, num_motifs, name):
        super().__init__(env)
        self.vocabulary = musicxmlio.select_random_motifs(filename, motif_length, num_motifs)
        self.name = name

    def play_sequence(self):
        m = random.choice(self.vocabulary)
        print(m)

        return m.notes

    def evaluate(self, artifact):
        pass

    async def act(self):
        # Writing concurrently to the dictionary should be ok as all agents write to different keys...
        self.env.add_music_to_part(self.name, self.play_sequence())
