# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

class Motif():
    """ Class that encapsulates a list of notes as a motif. """
    def __init__(self, notes):
        self.notes = notes

    def notes(self):
        return self.notes

    def similarity(self, other):
        """ Return similarity [0,1] 1 being exactly same """
        return 0.0