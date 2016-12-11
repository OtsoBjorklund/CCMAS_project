.. MACI documentation master file, created by
   sphinx-quickstart on Thu Dec  8 16:44:11 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Multi-Agents Collective Improvisation
================================

Description
----------------
The purpose of the system is to model collective musical improvisation, or so-called “free improvisation”. The agents use a commonly used improvisation technique called motific improvisation: their playing is based on the use motifs. In this case the motifs are just short segments of music instead of the more strict definition of motif in music theory. Each of the agents has a vocabulary of motifs which they use. The agents learn the motifs from MusicXML files which form the inspirational set. The agents can also transform the motifs they have learned and learn new motifs from the other agents in the process of the simulation.

The simulation proceeds so that each agent evaluates what has been played previously and then chooses a motif to play based on that. The agents are not aware of everything that has happened during the simulation, i.e. the agents have limited musical memory and are not able to listen to all other agents at the same time.

The result of the entire improvisation is output into a MusicXML file that can then be analysed and played using any music notation software.

Installation
----------------
The requirements for the system are specified in the file requirements.txt. music21 may produce warnings about libraries when the simulation is run, but the system does not use any of the functions of music21 that require additional libraries so the warnings can be ignored.

Running the system
----------------
The system is run by executing the script simulation.py. It does not take any arguments. The output is saved in the directory output.




.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

