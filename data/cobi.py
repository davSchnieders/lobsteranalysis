from data.two_center_interaction import TwoCenterInteraction


class COBI(TwoCenterInteraction):

    def __init__(self):
        TwoCenterInteraction.__init__(self, 'COBICAR.lobster', 'ICOBILIST.lobster', 'COBI')