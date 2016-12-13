# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random


class Memory():
    """ The memory of the agents. Container class for Motifs. Is iterable.

        :param capacity: The maximum number of motifs that can be remembered.
        :type capacity: int """

    def __init__(self, capacity):
        self._motifs = []
        self._capacity = capacity

    @property
    def capacity(self):
        return self._capacity

    def memorize(self, motif, step=0, replace_most_similar=True):
        """ Add new motif to memory. If memory is full replace the most similar or oldest motif with the new one.

            :param motif: Motif to be added to memory.
            :type motif: Motif
            :param step: The step of simulation in which the motif was added.
            :type step: int
            :param replace_most_similar: When memory is full, if this is true the new motif replaces the most similar
                motif in memory. If this is false, then replaces the oldest motif: the one with smallest step.
            :type replace_most_similar: bool """

        if len(self._motifs) < self._capacity:
            self._motifs.append((motif, step))
        else:
            if replace_most_similar:
                # Replace most similar motif with new motif
                index = self.index_of_most_similar(motif)
            else:
                # Replace oldest, ie with smallest step
                index = self.index_of_oldest()

            self._motifs[index] = (motif, step)

    def get_random_motif(self):
        """ Choose a random Motif from the memory.

            :return: Randomly selected motif.
            :rtype: Motif """
        random_elem = random.choice(self._motifs)
        return random_elem[0]

    def find_most_similar(self, m):
        """ Find the motif from memory that is the most similar to m.

            :param m: The query motif
            :type m: Motif """

        index = self.index_of_most_similar(m)
        return self._motifs[index][0]

    def find_least_similar(self, m):
        """ Find the motif that is least similar to m.

            :param m: The query motif
            :type m: Motif """

        # Similarity rating is at most 1.0 so start off with value 1.1
        min_similarity = 1.1
        for entry in self._motifs:
            motif = entry[0]
            similarity = motif.similarity(m)
            if similarity < min_similarity:
                min_similarity = similarity
                least_similar = motif

        return least_similar

    def index_of_oldest(self):
        """ Find the motif with the smallest step, i.e. the one that is oldest. """
        if not self._motifs:
            return 0

        index = 0
        min_step = self._motifs[0][1]
        for i in range(0, len(self._motifs)):
            step = self._motifs[i][1]
            if step < min_step:
                index = i
                min_step = step

        return index

    def index_of_most_similar(self, m):
        """ Find the index of the motif in memory that is most similar to m.

            :param m: The query motif
            :type m: Motif """

        max_similarity = 0.0
        index = 0
        for i in range(0, len(self._motifs)):
            motif = self._motifs[i][0]
            sim = motif.similarity(m)
            if sim > max_similarity:
                max_similarity = sim
                index = i

        return index

    def __iter__(self):
        """ Provides an iterator that iterates over the Motifs only. """
        class MemoryIterator:
            def __init__(self, tuple_list):
                self._tuple_list = tuple_list
                self._index = 0

            def __next__(self):
                if self._index < len(self._tuple_list):
                    motif = self._tuple_list[self._index][0]
                    self._index += 1
                    return motif
                else:
                    raise StopIteration()

        return MemoryIterator(self._motifs)

    def __len__(self):
        """ Number of motifs in memory. """
        return len(self._motifs)
