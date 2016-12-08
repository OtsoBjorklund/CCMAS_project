# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.

import random
from music21.note import Rest
from copy import deepcopy


class Motif:
    """ Class that encapsulates a list of music21.note.Note and music21.note.Rest objects as a motif.

        The agents handle all of their playing by using Motif objects. """

    def __init__(self, notes):
        self._notes = notes
        self._string_representation = self.get_string_representation()

    def __deepcopy__(self, memodict={}):
        """ Create a deepcopy of Motif """
        copied_notes = []
        for notation_elem in self._notes:
            copied_notes.append(deepcopy(notation_elem))

        return Motif(copied_notes)

    @property
    def notes(self):
        return self._notes

    def __str__(self):
        """ String representation of the motif. """
        return self._string_representation

    def get_string_representation(self):
        """ Create a transposition invariant string representation of motif.
            The representation ignores octaves and treats durations relatively.

            :return: String of interval and duration numbers.
            :rtype: str """

        string_repres = ''

        # Find last note so that the first note is compared circularly in relation to the last.
        # Keep the pitch and duration of previous notation element separately to enable comparisons
        # with both notes and rests.

        for i in range(len(self.notes) - 1, -1, -1):
            if self.notes[i].isNote:
                prev_pitch = self.notes[i].pitch
                prev_dur = self.notes[i].duration.quarterLength
                break
            else:
                prev_dur = self.notes[i].duration.quarterLength

        for notation_elem in self._notes:
            if notation_elem.isNote:
                # Compute the interval between this note and the previous as an integer string.
                interval = str(prev_pitch.pitchClass - notation_elem.pitch.pitchClass)
                # Compute the relation of the duration of this note and the duration of the previous note.
                # This tells by what factor the duration changes when moving from prev_note to this note.
                duration_relation = str(notation_elem.duration.quarterLength/prev_dur)

                string_repres += interval + duration_relation
                prev_pitch = notation_elem.pitch
                prev_dur = notation_elem.duration.quarterLength
            else:
                # For rests use r and the relative change in duration when compared to last note. This does not handle
                # multiple consecutive rests very well, fortunately they are quite rare.
                string_repres += 'r' + str(notation_elem.duration.quarterLength/prev_dur)
                prev_dur = notation_elem.duration.quarterLength

        return string_repres

    def similarity(self, other):
        """ Evaluate the similarity of this motif to other using Levenshtein distance of string representations.

         :param other: The motif that this motif is compared to.
         :type other: Motif object.
         :return: Similarity measurement in range [0,1] where 0 is not at all similar and 1 is exact match.
         :rtype: float """

        sim = 1 - (Motif.levenshtein(str(self), str(other)) / max(len(str(self)), len(str(other))))
        return sim

    def fit_into_context(self, context):
        """ How well the motif fits into a musical context.

        :param context: The context against which the fit of this motif is compared.
        :type context: A list of motifs.
        :return: A rating in the range [0, 1] with 0 being a very bad fit and 1 being a very good fit.
        :rtype: float """

        # If context is empty then cannot really fit or not fit. Return 0.5.
        if not context:
            return 0.5

        # Compute the average similarity to other motifs in the musical context
        avg_similarity = 0.0
        for motif in context:
            avg_similarity += self.similarity(motif)
        avg_similarity /= len(context)

        return avg_similarity

    @staticmethod
    def get_rest(length_quarters):
        """ Create a rest of length_quarters.

            :param length_quarters: Length of rest in quarter notes.
            :type length_quarters: Float.
            :return: Rest of length_quarters.
            :rtype: Motif """

        rest = Rest()
        rest.duration.quarterLength = length_quarters
        return Motif([rest])

    @staticmethod
    def transpose(motif, steps):
        """ Transpose motif up or down steps half-steps. Returns a transposed copy.

            :param motif: Motif that is transposed
            :type motif: Motif
            :param steps: Number of steps to be transposed. Positive values transpose up and
                negative values transpose down.
            :type steps: Integer.
            :return: A transposed copy of motif
            :rtype: Motif object. """

        # Deepcopy the motif and get its notes to ensure the original motif is unaffected
        notes = deepcopy(motif).notes
        for notation_elem in notes.notes:
            # Only notes can be transposed.
            if notation_elem.isNote:
                notation_elem.pitch.transpose(steps, inPlace=True)

        return Motif(notes)

    @staticmethod
    def transpose_random_note(motif):
        """ Transposes a random note of the motif. Returns a copy.

            :param motif: Motif whose note is transposed
            :type motif: Motif
            :return: A transposed copy of motif
            :rtype: Motif """

        # Deepcopy the motif and get its notes to ensure the original motif is unaffected
        notes = deepcopy(motif).notes

        # Select a random note
        for _ in range(0, len(notes)):
            random_note = random.choice(notes)
            if random_note.isNote:
                transposition = random.randint(-12, 12)
                random_note.transpose(transposition, inPlace=True)
                break

        return Motif(notes)

    @staticmethod
    def levenshtein(s, t):
        """ Compute the edit distance between two strings.
            From Wikipedia article; Iterative with two matrix rows.
            Copied from course material. """
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
