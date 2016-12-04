# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

class Motif():
    """ Class that encapsulates a list of notes as a motif. """
    def __init__(self, notes):
        self._notes = notes
        # TODO: The string representation could cached and initialized lazily.
        # self._string_representation

    @property
    def notes(self):
        return self._notes

    def transpose(self, steps):
        """ Transpose motif up or down steps half-steps.

         :param steps: Number of steps to be transposed. Positive values tranpose up and negative values tranpose down.
         :type steps: Integer. """

        for notation_elem in self._notes:
            # Only notes can be transposed.
            if notation_elem.isNote:
                notation_elem.pitch.transpose(steps)

    def __str__(self):
        """ String representation of the motif. """
        return self.get_string_representation()

    def get_string_representation(self):
        string_repres = ''
        for notation_elem in self._notes:
            if notation_elem.isNote:
                string_repres += str(notation_elem.pitch) + str(notation_elem.duration.quarterLength)
            else:
                string_repres += str(notation_elem.duration.quarterLength)

        return string_repres

    def levenshtein(self, s, t):
        """
        TODO: Use a more specific method from Lemström.
        This is copied from course material.

        Compute the edit distance between two strings.
        From Wikipedia article; Iterative with two matrix rows.
        """
        if s == t:
            return 0
        elif len(s) == 0:
            return len(t)
        elif len(t) == 0:
            return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]

        return v1[len(t)]

    def similarity(self, other):
        """ Evaluate the similarity of this motif to other using Levenshtein distance of string representations.

         :param other: The motif that this motif is compared to.
         :type other: Motif object.
         :return: Similarity measurement in range [0,1] where 0 is not at all similar and 1 is exact match.
         :rtype: Float. """

        sim = 1 - (self.levenshtein(str(self), str(other)) / max(len(str(self)), len(str(other))))
        return sim