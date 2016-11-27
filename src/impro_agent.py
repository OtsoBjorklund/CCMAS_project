# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

from creamas import CreativeAgent
import src.musicxmlio
import random
from src.motif import Motif


class ImprovisingAgent(CreativeAgent):

    def __init__(self, env, filename, motif_length, num_motifs, name):
        super().__init__(env)
        self.vocabulary = self.learn_vocabulary(filename, motif_length, num_motifs)
        self.name = name

    def learn_vocabulary(self, filename, motif_length, num_motifs):
        """ Select random sequences of notes as motifs from the musicXML file """
        notelist = src.musicxmlio.read_musicxml_to_list(filename)
        motif_list = []

        for _ in range(0, num_motifs):
            rand_index = random.randint(0, len(notelist) - motif_length)
            notes = []
            for i in range(rand_index, rand_index + motif_length):
                notes.append(notelist[i])

            motif_list.append(Motif(notes))

        return motif_list

    def play_sequence(self):
        return random.choice(self.vocabulary).notes

    def evaluate(self, artifact):
        pass

    async def act(self):
        pass
