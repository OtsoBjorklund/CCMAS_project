
class Memory():
    """ The memory of the agents. Container class for Motifs. """

    def __init__(self, size):
        self._motifs = []
        self._size = size

    def memorize(self, motif):
        """ Add new motif to memory. If memory is full replace the most similar motif with the new one. """
        if len(self._motifs) < self._size:
            self._motifs.append(motif)
        else:
            # Replace most similar motif with new motif
            index = self.index_of_most_similar(motif)
            self._motifs[index] = motif

    def find_most_similar(self, m):
        """ Find the motif from memory that is the most similar to m. """
        index = self.index_of_most_similar(m)
        return self._motifs[index]

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