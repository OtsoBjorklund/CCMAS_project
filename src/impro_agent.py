# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random
from memory import Memory

from creamas import CreativeAgent, Artifact
from motif import Motif


import musicxmlio


class ImprovisingAgent(CreativeAgent):

    def __init__(self, env, insp_set, motif_length, memory_size, name):
        super().__init__(env)
        self._name = name
        self._motif_length = motif_length
        self._last_motif = None
        self._vocabulary = self.create_vocabulary(insp_set, motif_length)
        # What the agent remembers of other agents playing
        self._memory_of_situation = Memory(memory_size)

        # The overall evaluation of the agent by itself
        self._sum_of_evaluations = 0.0
        self._motifs_played = 0
        self._confidence = random.random()

    def create_vocabulary(self, insp_set, motif_length):
        """ Choose random motifs of length motif_length from randomly selected files defined in insp_set.

         """

        # Dictionary of how many motifs to be selected from each file.
        files = {}
        # Total number of motifs
        num_motifs = 0

        for directory in insp_set:
            motifs_from_file = insp_set[directory]
            num_motifs += motifs_from_file
            filename = musicxmlio.get_random_filename('inspirational_sets/' + directory + '/')
            files[filename] = motifs_from_file

        print('Inspirational set for', self.name, '\n', files)

        random_motifs = []
        for filename in files:
            motifs_from_file = musicxmlio.select_random_motifs(filename, motif_length, files[filename])
            for m in motifs_from_file:
                random_motifs.append(m)

        memory = Memory(num_motifs)
        for m in random_motifs:
            memory.memorize(m)

        return memory

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

        modified_motif = Motif.get_random_variation(best_motif)
        mod_motif_eval = self.evaluate(Artifact(self, obj = modified_motif, domain = 'music'))
        if mod_motif_eval >= best_evaluation:
            best_motif = modified_motif
            print('Modified motif used')
            self._vocabulary.memorize(best_motif)

        best_motif = Motif.transpose_to_key_of_context(best_motif, self._memory_of_situation)

        # Todo: improve the evaluation of the overall performance
        overall_performance = (self._sum_of_evaluations + best_evaluation) / (self._motifs_played + 1)
        if overall_performance < self._confidence:
            best_motif = Motif.get_rest(self._motif_length)
            self._confidence = 0.0
        else:
            self._confidence = overall_performance

        return best_motif

    def listen_to_others(self, musical_context):
        """ Update the agent's knowledge of the musical situation. """
        # Todo: come up with a more sensible way of handling the knowledge of musical context
        for motif in musical_context:
            self._memory_of_situation.memorize(motif)

    def surprisingness(self, motif):
        # TODO: Kari
        return 0.5

    def evaluate(self, artifact):
        """ Evaluate how good the previously played motif was when compared to what others played.  """
        # TODO: Evaluate based on fit AND surpise
        own_motif = artifact.obj
        fit = own_motif.fit_into_context(self._memory_of_situation)
        return fit

    async def act(self):
        """ Play motif, set it as the last motif played by the agent and add it to the environment. """
        motif = self.play_motif()
        self._last_motif = motif
        # Writing concurrently to the dictionary should be ok as all agents write to different keys.
        self.env.add_music_to_part(self.name, motif)
