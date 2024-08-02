from data.two_center_interaction import TwoCenterInteraction


class COHP(TwoCenterInteraction):

    def __init__(self):
        TwoCenterInteraction.__init__(self, 'COHPCAR.lobster', 'ICOHPLIST.lobster', 'COHP')
        self.xlabel = "$-$COHP (eV)"
        for interaction, cohp in self.interactions.items():
            cohp['plot'] = -1.0 * cohp['plot']
            cohp['integrated_plot'] = -1.0 * cohp['integrated_plot']
