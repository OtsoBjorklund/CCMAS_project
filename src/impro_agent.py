# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random

from creamas import CreativeAgent, Artifact
from motif import Motif

import musicxmlio


class ImprovisingAgent(CreativeAgent):

    def __init__(self, env, filename, motif_length, num_motifs, name):
        super().__init__(env)
        self._name = name
        self._motif_length = motif_length
        # Todo: vocabulary should be a Memory object
        self._vocabulary = self.create_vocabulary(filename, motif_length, num_motifs)
        # What the agent remembers of other agents playing
        self._memory_of_situation = []

        # The overall evaluation of the agent by itself
        self._sum_of_evaluations = 0.0
        self._motifs_played = 0
        self._overall_performance = 0.0

    def create_vocabulary(self, filename, motif_length, num_motifs):
        # Todo: Enable learning from multiple files.
        return musicxmlio.select_random_motifs(filename, motif_length, num_motifs)

    @property
    def name(self):
        return self._name

    def play_motif(self):
        """ Find motif with the best evaluation """
        best_motif = None
        best_evaluation = 0.0
        for motif in self._vocabulary:
            evaluation = self.evaluate(Artifact(self, obj=motif, domain='music'))
            if evaluation > best_evaluation:
                best_motif = motif
                best_evaluation = evaluation

        # Todo: Try variations and improving the motif using them

        # Todo: improve the evaluation of the overall performance
        overall_performance = (self._sum_of_evaluations + best_evaluation) / (self._motifs_played + 1)
        if overall_performance <= self._overall_performance - 0.01:
            best_motif = Motif.get_rest(self._motif_length)

        self._overall_performance = overall_performance

        return best_motif

    def listen_to_others(self, musical_context):
        """ Update the agent's knowledge of the musical situation. """
        # Todo: come up with a more sensible way of handling the knowledge of musical context
        num_motifs = 3
        self._memory_of_situation = random.sample(musical_context, num_motifs)

    def evaluate(self, artifact):
        """ Evaluate how good the previously played motif was when compared to what others played.  """
        own_motif = artifact.obj
        fit = own_motif.fit_into_context(self._memory_of_situation)
        return fit

    async def act(self):
        # Writing concurrently to the dictionary should be ok as all agents write to different keys...
        self.env.add_music_to_part(self.name, self.play_motif())
