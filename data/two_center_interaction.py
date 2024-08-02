import numpy as np
import matplotlib.pyplot as plt
import fnmatch
import re


class TwoCenterInteraction:

    def __init__(self, two_center_interaction_filename, two_center_integration_filename, type='Two Center Interaction'):
        self.interactions = {}
        self.energies = []
        self.true_e_min = None
        self.true_e_max = None
        self.e_fermi = None
        self.n_points = None
        self.type = type
        self.xlabel = type
        self._read_plots_from_file(two_center_interaction_filename)
        self._read_integrations_from_file(two_center_integration_filename)

    def get_states(self):
        return [(interaction, self.interactions[interaction]['integrated_value']) for interaction in self.interactions.keys()]

    def print_plot(self, states_string, e_range=[]):
        """
        Plots the all two center interaction plots requested in states_string and safes the plot to eps file.

        Args:
            states_string: States to plot.
            e_range: Energy range to plot along the y axis.

        Returns: Nothing.

        """
        max_int_val = 0.0
        min_int_val = 9999999.999
        fig, ax = plt.subplots()
        fig.set_size_inches(8.0,12.0)
        for interaction in states_string.split():
            this_interaction = np.array([0.0 for i in range(self.n_points)])
            for sub_interaction in interaction.split("+"):
                matched_states = fnmatch.filter(self.interactions.keys(), sub_interaction)
                if len(matched_states) == 0:
                    print("WARNING: No states matched for {state}".format(state=sub_interaction))
                for matched_state in matched_states:
                    this_interaction += self.interactions[matched_state]['plot']
            max_int_val = max(max_int_val, this_interaction.max())
            min_int_val = min(min_int_val, this_interaction.min())
            ax.plot(this_interaction, self.energies, label=interaction)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel("Energy (eV)")
        if e_range:
            ax.set_ylim([int(y) for y in e_range.split()])
        ax.set_xlim([min_int_val/0.9, max_int_val/0.9])
        ax.axhline(y=0.0, color='black', linestyle='--')
        ax.axvline(x=0.0, color='black', linestyle='-')
        ax.text(ax.get_xlim()[1]/0.90, 0, "$\epsilon_\mathrm{F}$", color="black", ha="right", va="center")
        ax.legend(fontsize=14)
        fig.savefig("{type}.eps".format(type=self.type), format='eps', dpi=100, bbox_inches='tight')

    def _read_plots_from_file(self, filename):
        with open(filename, 'r') as two_center_interaction_file:
            two_center_interaction_file.readline()
            info_line = two_center_interaction_file.readline().split()
            n_interactions = int(info_line[0])
            n_spin = int(info_line[1])
            self.n_points = int(info_line[2])
            self.true_e_min = float(info_line[3])
            self.true_e_max = float(info_line[4])
            self.e_fermi = float(info_line[5])
            interactions = []
            for i in range(n_interactions):
                interaction_string = two_center_interaction_file.readline()
                interaction = "Average"
                dist = None
                x = re.search('.*\.[0-9]*:([a-zA-Z]*)([0-9]*)->([a-zA-Z]*)([0-9]*)\((\d*.\d*)\)', interaction_string)
                x_orbitalwise = re.search('.*\.[0-9]*:([a-zA-Z]*)([0-9]*)\[([0-9]*[a-z].*)\]->([a-zA-Z]*)([0-9]*)\[([0-9]*[a-z].*)\]\((\d*.\d*)\)', interaction_string)
                if x is not None:
                    interaction = "{left}->{right}".format(left=".".join([x.group(i) for i in range(1, 3)]),right=".".join([x.group(i) for i in range(3, 5)]))
                    dist = float(x.group(5))
                elif x_orbitalwise is not None:
                    interaction = "{left}->{right}".format(left=".".join([x_orbitalwise.group(i) for i in range(1, 4)]),right=".".join([x_orbitalwise.group(i) for i in range(4, 7)]))
                    dist = float(x_orbitalwise.group(7))
                interactions.append(interaction)
            self.energies = np.zeros(self.n_points)
            two_center_interactions = np.zeros((self.n_points, n_interactions * 2 * n_spin))
            for i_point in range(self.n_points):
                this_line_floats = [float(i) for i in two_center_interaction_file.readline().split()]
                self.energies[i_point] = this_line_floats[0]
                two_center_interactions[i_point] = this_line_floats[1:]
            for i, interaction in enumerate(interactions):
                self.interactions[interaction] = {
                    'plot': np.array(two_center_interactions[:, i*2]),
                    'integrated_plot': np.array(two_center_interactions[:, i*2+1]),
                    'dist': dist
                }

    def _read_integrations_from_file(self, filename):
        with open(filename, 'r') as two_center_interaction_file:
            two_center_interaction_file.readline()
            two_center_interaction_file.readline()
            average = 0.0
            for interaction_name in self.interactions.keys():
                if interaction_name == "Average":
                    continue
                line = two_center_interaction_file.readline().split()
                self.interactions[interaction_name]['integrated_value'] = line[7]
                average += float(line[7])

            self.interactions['Average']['integrated_value'] = average/(len(self.interactions.keys())-1)
