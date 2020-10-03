.. MACI documentation master file, created by
   sphinx-quickstart on Thu Dec  8 16:44:11 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Multi-Agent Collective Improvisation (MACI)
================================

Description
----------------
The purpose of the system is to model collective musical improvisation, or so-called “free improvisation”. The agents
use a commonly used improvisation technique called motific improvisation: their playing is based on the use motifs.
In this case the motifs are just short segments of music. Musical data is handled entirely in symbolic form in the
system.
The focus of the system is on the interaction of the agents.

The Process of Improvisation
----------------
Before the simulation (the improvisation), begins, the agents learn vocabularies of motifs from a set of MusicXML
files. The selection of files from which an agent learns its motifs forms the inspirational set of that agent. During
the improvisation, on each step the agents select a motif to play from their vocabularies.
The choice is based on what the agent would consider to fit best into the musical context of the environment. The
agents can perceive and remember a limited number of motifs from the environment. These motifs form the musical
context, or framing, for the evaluation of fit. The agents have a property called confidence level which describes
how confident the agent is in its own playing. The agents only produce a motif if they consider it to boost their
confidence, otherwise they produce a rest (silence). The confidence of the agent declines as it stays quiet, so the
longer the agent stays quiet the more likely it is to find a motif to play from its vocabulary that would boost its
confidence. The agents also try improving the motifs by making random variations of them. The agents can also
randomly decide to do something random or contrary to the most fitting choice in order to keep the music
lively and avoid all agents converging to playing the same thing.

After all agents have played their motifs on the step, they evaluate how well what they did actually fit into the
context and update their confidence level. The agents also learn new motifs from the other agents by memorizing the
most surprising motifs from the context if they are evaluated better than what the agent itself last played. There is
no global evaluation of the entire improvisation, the agents only evaluate their own playing and the most surprising
motifs played by the other agents.

The agents have two different memories: one for the vocabulary and one for the motifs perceived from the environment.
When the agents add motifs to their vocabulary, the new motif replaces the most similar one to keep the vocabulary
diverse. When the agents memorize motifs from the environment, they replace the oldest motifs from their memory of
the musical context.

Implementation
----------------
The system is implemented using python 3, creamas, and music21.
The improvisation lasts a predetermined number of steps and the motif length is fixed and is the same for all agents.
The result of the entire improvisation is output into a
MusicXML and MIDI file that can then be viewed and played by many music notation and digital audio workstation
(DAW) applications. All handling of symbolic music data is handled by the class Motif. All agents use same length
motifs so that there is no need for any separate rhythmic synchronisation between the agents.

The system is truly a multi-agent system: there is no global authority controlling the agent's decision making, and
the communication between the agents is limited to perceiving only some of the motifs from the environment. The
communication is also limited to playing and listening as the only information the agents share with each other are
the motifs they play.
The downside of this is that there is no automatic evaluation of the entire output of the system, therefore making
manual evaluation by a human necessary.

Installation
----------------
Installing the system requires downloading the source files and installing the requirements.
The requirements for the system are specified in the file requirements.txt.
The requirements can be installed using pip::

    pip install -r requirements.txt

It is recommended to create a virtual environment and install the requirements in the virtual environment.
music21 may produce warnings about some libraries
when the simulation is run, but the system does not use any of the functions of music21 that require additional
libraries so the warnings can be ignored.

Running the system
----------------
The system is run by (activating virtual env) moving into the directory src and executing::

    python simulation.py

The system does not take any arguments. The output is saved into the directory src/output.
Changing the configuration of the system requires changing the file simulation.py. The number of steps, length of
motif, and the attributes of the agents can be adjusted to produce different outcomes. These variables are described
in more detail in the documentation for the modules.


.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

