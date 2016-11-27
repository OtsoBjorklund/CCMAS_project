# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

class Motif():
    """ Class that encapsulates a list of notes as a motif. """
    def __init__(self, notes):
        self.notes = notes

    def notes(self):
        return self.notes