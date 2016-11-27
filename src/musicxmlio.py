# MACI. Course project for Computational Creativity and Multi-Agent Systems. Fall 2016.
# Otso Björklund, Kari Korpinen, Cedric Rantanen.
#
# Functions for handling MusicXML

import music21


def read_musicxml_to_list(filepath):
    """ Read all the parts in the MusicXML file and return a list of note or rest objects. """

    score = music21.converter.parse(filepath)
    notelist = []

    # Go through parts and append all notes and rests to the list
    for part in score.parts:
        elems = part.flat.elements
        for element in elems:
            if type(element) is music21.note.Note:
                notelist.append(element)

            if type(element) is music21.note.Rest:
                notelist.append(element)

    return notelist


def parts_dictionary_to_musicxml(parts, filename):
    """ Write the parts into a MusicXML file with name filename. """
    score = music21.stream.Score()

    # Write each part separately into the file
    for partname in parts:
        notation_elements = parts[partname]
        part = music21.stream.Part()

        # Set part id and partName
        part.id = partname
        part.partName = partname

        # Append the notes from the list of notes to the part
        # The notes have to be deep copied, because music21 cannot insert the same note object twice into a stream when
        # writing to a file.
        for notation_elem in notation_elements:
            # If the element is a rest, create a new rest with the same duration and append it to the part.
            if notation_elem.isRest:
                new_rest = music21.note.Rest()
                new_rest.duration.quarterLength = notation_elem.duration.quarterLength
                part.append(new_rest)
            else:
                # Else it must be a note. Create a new note and append it to the part.
                new_note = music21.note.Note(notation_elem.nameWithOctave)
                new_note.duration.quarterLength = notation_elem.duration.quarterLength
                part.append(new_note)

        # Insert part to score
        score.insert(0, part)

    # Write score to file
    score.write('musicxml', filename)



