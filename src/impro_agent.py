# MACI.
# Otso Björklund.

from math import floor
from memory import Memory
from creamas import CreativeAgent, Artifact
from motif import Motif
import random
import musicxmlio


class ImprovisingAgent(CreativeAgent):
    """ Agent class that improvises music based on motifs.

        The agent has a fixed size vocabulary that it learns from files selected randomly from
        the directories specified by inspiring set. The agent plays motifs by selecting them from its vocabulary
        and making variations of them. The agent can also learn new motifs from the environment.

        The agent evaluates its own performance using the variable confidence which is the average of all evaluations
        the agent has made of its own playing. The agents play motifs only if they think that it would improve their
        confidence level.

          :param env: The environment that the ImprovisingAgent acts in.
          :type env: Environment
          :param insp_set: The inspiring set from which the agent learns its vocabulary.
            Dictionary of directories and integers, dir:n, meaning select n motifs from a file randomly selected from dir.
          :type insp_set: dict
          :param motif_length: The length of the motifs the agent uses in quarter note lengths.
          :type motif_length: float
          :param name: The name of the agent.
          :type name: str
          :param pr_of_contrast: Probability that the agent decides to play something contrasting. This tells how ready
            the agent is to play something that is opposite to what it perceives from the environment.
          :type pr_of_contrast: float
          :param conf_decline_factor: By what factor the confidence of the agent decreases when it stays silent.
            The confidence is multiplied by this when the agent stays silent, should be in the range [0,9).
          :type conf_decline_factor: float
          :param conf_th: By what factor estimated confidence of playing a motif must exceed the
            current confidence level. Value between [0,1], preferably quite small.
          :type conf_th: float """

    def __init__(self, env, insp_set, motif_length, memory_size, name, pr_of_contrast=0.2,
                 conf_decline_factor=0.6, conf_th=0.1):
        super().__init__(env)
        self._name = name
        self._motif_length = motif_length

        # The vocabulary that the agent learns from the inspiring set
        self._vocabulary = self.create_vocabulary(insp_set, motif_length)

        # What the agent remembers of other agents playing
        self._memory_of_situation = Memory(memory_size)

        # These are used to evaluate the agents idea of its own playing and confidence.
        self._sum_of_evaluations = 0.0
        # Begin from 1 to avoid dividing by zero.
        self._steps_acted = 1
        # Start with a random level of confidence.
        self._confidence = random.random()

        # The previous motif that the agent played.
        self._last_motif = None

        self._pr_of_contrast = pr_of_contrast
        self._confidence_decline_factor = conf_decline_factor
        self._confidence_threshold = conf_th

    def create_vocabulary(self, insp_set, motif_length):
        """ Chooses random motifs of length motif_length from randomly selected files
            from directories defined in insp_set.
            Used for creating the agent's vocabulary.

            :param insp_set: How many motifs to pick randomly from a randomly selected file in a directory.
                The keys are directory names and the values are the numbers of motifs.
            :type insp_set: dict
            :param motif_length: Length of motifs in quarter notes.
            :type motif_length: float
            :return: The vocabulary created from the inspiring set.
            :rtype: Memory """

        # Dictionary of how many motifs to be selected from each file.
        files = {}
        # Total number of motifs
        num_motifs = 0

        # Get random files from the directories specified by insp_set
        for directory in insp_set:
            motifs_from_file = insp_set[directory]
            num_motifs += motifs_from_file
            filename = musicxmlio.get_random_filename('inspirational_sets/' + directory + '/')
            files[filename] = motifs_from_file

        print('Inspirational set for', self.name, '\n', files)

        random_motifs = []
        for filename in files:
            motifs_from_file = musicxmlio.select_random_motifs(filename, motif_length, files[filename])
            for m in motifs_from_file:
                random_motifs.append(m)

        # Create memory and memorize motifs.
        memory = Memory(num_motifs)
        for m in random_motifs:
            memory.memorize(m)

        return memory

    @property
    def name(self):
        """ The name of the agent """
        return self._name

    @property
    def memory_capacity(self):
        """ The maximum number of motifs the agent can remember from the environment. """
        return self._memory_of_situation.capacity

    def play_motif(self):
        """ Find motif with the best evaluation from the agents vocabulary. Create a variation of the motif and see if it
            would be better. If the variation is better, memorize it and return it.
            Estimate if playing the motif would increase the agent's confidence level. If the motif is estimated to
            not increase the confidence level enough, the agent rests instead i.e. produces a motif that is all rests.
            With probability pr_of_contrast the agent plays something contrary to the context or random.

            :return: Motif with best evaluation.
            :rtype: Motif """

        motif_to_play = None
        best_evaluation = 0.0

        # Find motif with best evaluation from vocabulary
        for motif in self._vocabulary:
            evaluation = self.evaluate(Artifact(self, obj=motif, domain='music'))
            if evaluation > best_evaluation:
                motif_to_play = motif
                best_evaluation = evaluation

        # Get a random variation of the motif and see if it would be better than the original.
        variation = Motif.get_random_variation(motif_to_play)
        # If the variation is at least as good as the found best motif use it instead and memorize it.
        evaluation_of_variation = self.evaluate(Artifact(self, obj=variation, domain='music'))
        if evaluation_of_variation >= best_evaluation:
            motif_to_play = variation
            best_evaluation = evaluation_of_variation
            self._vocabulary.memorize(motif_to_play)

        # Estimate what the future confidence level would be if the agent played the motif
        estimate_of_future_confidence = (self._sum_of_evaluations + best_evaluation) / (self._steps_acted + 1)
        if estimate_of_future_confidence <= self._confidence * (1 + self._confidence_threshold):
            # If playing the motif would not increase confidence enough, rest.
            motif_to_play = Motif.get_rest(self._motif_length)

        # With probability of pr_of_contrast the agent decides to play something contrasting.
        play_contrasting = random.random()
        if play_contrasting <= self._pr_of_contrast:
            if not motif_to_play.is_all_rests():
                motif_to_play = self._vocabulary.find_least_similar(motif_to_play)
            else:
                # If there is no motif to contrast against, choose a random motif.
                motif_to_play = self._vocabulary.get_random_motif()

        # Keep track of the last motif played
        self._last_motif = motif_to_play

        # Transpose the best_motif based on key estimates.
        # The motifs are handled in a key invariant way so memorizing the transposed motif is unnecessary.
        return Motif.transpose_to_key_of_context(motif_to_play, self._memory_of_situation)

    def listen_to_others(self, musical_context, step):
        """ Update the agent's knowledge of the musical situation
            and evaluate how well the last played motif worked out.
            Learn surprising motifs from the musical context.
            Update the confidence level of the agent.

            :param musical_context: Motifs recently played in the environment.
            :type musical_context: list
            :param step: The step of the simulation.
            :type step: int """

        # Update the agent's memory of the situation by choosing random motifs from the musical_context and
        # putting them into the memory.
        num_motifs = min(self.memory_capacity, len(musical_context))
        perceived_motifs = random.sample(musical_context, num_motifs)
        for motif in perceived_motifs:
            # The perceived motifs replace oldest motifs in the memory.
            self._memory_of_situation.memorize(motif, step=step, replace_most_similar=False)

        # Find most surprising motif from the motifs perceived from environment
        most_surprising = None
        max_surprise = 0.0
        for motif in perceived_motifs:
            surprise = self.surprisingness(motif)
            if surprise > max_surprise:
                max_surprise = surprise
                most_surprising = motif

        # Evaluate how good the last own motif was.
        evaluation = self.evaluate(Artifact(self, obj=self._last_motif, domain='music'))

        # Check that an at all surprising motif was found and memorize the most surprising motif
        # as a random variation if it is evaluated better than own last motif.
        if most_surprising:
            if self.evaluate(Artifact(self, obj=most_surprising, domain='music')) > evaluation:
                self._vocabulary.memorize(Motif.get_random_variation(most_surprising))

        # Update the confidence level of the agent.
        self._sum_of_evaluations += evaluation
        self._confidence = self._sum_of_evaluations / self._steps_acted
        # If the agents last motif was a rest, the agent did not play anything
        # and the confidence level decreases even more.
        if self._last_motif.is_all_rests():
            self._confidence *= self._confidence_decline_factor

    def surprisingness(self, motif):
        """ Evaluate the surprisingness of motif by comparing how
            different it is to the most similar motif the agent knows.

            :param motif: The motif whose suprisingness is evaluated.
            :type motif: Motif
            :return: Rating in the range [0, 1] with 1 being most surprising.
            :rtype: float """

        most_sim = self._vocabulary.find_most_similar(motif)
        return 1 - most_sim.similarity(motif)
        
    def evaluate(self, artifact):
        """ Evaluate how good the motif was by considering how well it fit into what the agent
            remembers of other agent's playing.

            :param artifact: Artifact object containing a motif.
            :type artifact: Artifact """

        motif = artifact.obj
        return motif.fit_into_context(self._memory_of_situation)

    async def act(self):
        """ Play motif and add it to the environment. """

        motif = self.play_motif()
        # Writing concurrently to the dictionary should be ok as all agents write to different keys.
        self.env.add_music_to_part(self.name, motif)
        self._steps_acted += 1

