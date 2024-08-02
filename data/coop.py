from data.two_center_interaction import TwoCenterInteraction


class COOP(TwoCenterInteraction):

    def __init__(self):
        TwoCenterInteraction.__init__(self, 'COOPCAR.lobster', 'ICOOPLIST.lobster', 'COOP')