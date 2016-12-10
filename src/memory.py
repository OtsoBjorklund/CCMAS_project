# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random

class Memory():
    """ The memory of the agents. Container class for Motifs. """

    def __init__(self, size):
        self._motifs = []
        self._size = size

    def memorize(self, motif, replace_most_similar=True):
        """ Add new motif to memory. If memory is full replace the most similar motif with the new one. """
        if len(self._motifs) < self._size:
            self._motifs.append(motif)
        else:
            if replace_most_similar:
                # Replace most similar motif with new motif
                index = self.index_of_most_similar(motif)
            else:
                # Replace random
                index = random.randrange(0, len(self._motifs))

            self._motifs[index] = motif

    def find_most_similar(self, m):
        """ Find the motif from memory that is the most similar to m. """
        index = self.index_of_most_similar(m)
        return self._motifs[index]

    def find_least_similar(self, m):
        """ Find the motif that is least similar to m """
        min_similarity = 1.0
        for motif in self._motifs:
            similarity = motif.similarity(m)
            if similarity < min_similarity:
                min_similarity = similarity
                least_similar = motif

        return least_similar

    def index_of_most_similar(self, m):
        """ Find the index of the motif in memory that is most similar to m. """

        max_similarity = 0.0
        index = 0
        for i in range(0, len(self._motifs)):
            sim = self._motifs[i].similarity(m)
            if sim > max_similarity:
                max_similarity = sim
                index = i

        return index

    def __iter__(self):
        return self._motifs.__iter__()

    def __len__(self):
        return len(self._motifs)