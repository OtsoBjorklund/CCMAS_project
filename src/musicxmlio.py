# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#
# Functions for handling MusicXML IO.

import music21
import random
import os
from copy import deepcopy
from motif import Motif


def read_musicxml_to_list(filepath):
    """ Read all the parts in the MusicXML file and return a list of note or rest objects.
        Ignores everything other than Note and Rest objects. The parts are concatenated to each other
        so that parts that were simultaneous in the score are sequential in the list.

        :param filepath: The path to the MusicXML file to be read.
        :type filepath: String.
        :return: Returns a list of notes and rests.
        :rtype: List of music21.note.Note and music21.note.Rest objects. """

    # Read the file to a music21.stream object.
    score = music21.converter.parse(filepath)
    notelist = []

    # Go through parts and append all notes and rests to the list
    for part in score.parts:
        notation_elements = part.flat.elements
        for element in notation_elements:
            # Append only objects of type Note or Rest.
            if type(element) is music21.note.Note or type(element) is music21.note.Rest:
                # Filter out grace notes with duration 0.
                if element.duration.quarterLength != 0:
                    notelist.append(element)

    return notelist


def parts_to_musicxml_midi(parts, filename):
    """ Write the parts dictionary into a MusicXML file and MIDI file with name filename.
        Each part in the parts will be its own part in the MusicXML score and its own channel in MIDI file.

        :param parts: The parts to be written in to the score.
        :type parts: Dictionary with strings as keys and lists of Motif objects as
            values. The keys will be used as part names in the score.
        :param filename: filename for the MusicXML file.
        :type filename: String. """

    # Create score and then append the parts into it.
    score = music21.stream.Score()

    # Add the parts to the score in the order of part name
    ordered_part_names = sorted(parts)

    # Write each part separately into the score
    for partname in ordered_part_names:
        motif_list = parts[partname]
        part = music21.stream.Part()

        # Set part id and partName
        part.id = partname
        part.partName = partname

        # Append the notes/rests from the list of motifs
        # The notes have to be deep copied, because music21 cannot insert the same note object twice into a stream when
        # writing to a file.
        for motif in motif_list:
            for notation_elem in motif.notes:
                copied_elem = deepcopy(notation_elem)
                # Set stem direction to None so that the notation program can set the stem directions intelligently.
                copied_elem.stemDirection = None
                part.append(copied_elem)

        # Insert part to score
        score.insert(0, part)

    # Write score to MusicXML file
    score.write('musicxml', filename + '.xml')
    # Write score to MIDI file
    score.write('midi', filename + '.midi')


def get_random_filename(path):
    """ Get the relative path of a random file from directory specified by path.
        :param path: The path of the directory from which to select random file.
        :type path: str
        :return: Path to randomly selected file.
        :rtype: str """
    return path + random.choice(os.listdir(path))


def select_random_motifs(filename, motif_length, num_motifs):
    """ Select random sequences of notes as motifs from a MusicXML file.

        :param filename: Name of the file from which motifs will be selected.
        :type filename: String.
        :param motif_length: The length of the motifs to be selected in quarter notes.
        :type motif_length: Float.
        :param num_motifs: Number of motifs to be selected from file.
        :type num_motifs: Integer.
        :return: List of num_motifs motifs with length motif_length.
        :rtype: List of motif.Motif objects. """

    notelist = read_musicxml_to_list(filename)
    motif_list = []

    for _ in range(0, num_motifs):
        rand_index = random.randint(0, len(notelist))
        notes = []
        cumulated_duration = 0.0

        # Keep track of the whole duration of selected notes in cumulated_duration.
        while cumulated_duration < motif_length:
            if rand_index < len(notelist):
                notation_elem = notelist[rand_index]
                rand_index += 1

                if cumulated_duration + notation_elem.duration.quarterLength <= motif_length:
                    # If the duration of the selected notation element is short enough add it to the notes.
                    cumulated_duration += notation_elem.duration.quarterLength
                    notes.append(notation_elem)
                else:
                    # If the new element (note/rest) is too long in duration create a new one with shortened duration.
                    # Handle Note and Rest objects separately.
                    if notation_elem.isRest:
                        shortened_elem = music21.note.Rest()
                        shortened_elem.duration.quarterLength = motif_length - cumulated_duration
                    else:
                        shortened_elem = music21.note.Note(notation_elem.nameWithOctave)
                        shortened_elem.duration.quarterLength = motif_length - cumulated_duration

                    # Have to check for zero, because float roundings with tuplet rhythms might lead to situations where
                    # a note or rest is created with duration 0.0.
                    # What a horrible idea to use floats instead of rational numbers for durations in notation data...
                    if shortened_elem.duration.quarterLength != 0.0:
                        notes.append(shortened_elem)

                    # Motif is full so stop.
                    break
            else:
                # If the random index has gone beyond the list, complete the motif with a rest.
                rest = music21.note.Rest()
                rest.duration.quarterLength = motif_length - cumulated_duration

                # Have to check for zero, due to problems with music21 duration arithmetic.
                if rest.duration.quarterLength != 0.0:
                    notes.append(rest)
                break

        # Create a Motif from the notes and append it to the list.
        motif_list.append(Motif(notes))

    return motif_list
