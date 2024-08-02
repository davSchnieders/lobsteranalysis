

class PopulationAnalysis:

    def __init__(self):
        self.charges = []
        self.gross_populations = []
        self._read_charge_file('CHARGE.lobster')
        self._read_gross_populations('GROSSPOP.lobster')

    def _read_charge_file(self, filename):

        with open(filename, 'r') as charge_file:
            charge_file.readline()
            charge_file.readline()
            charge_file.readline()
            while True:
                line = charge_file.readline().split()
                if len(line) == 0:
                    break
                self.charges.append({
                    'element': line[1],
                    'mulliken_charge': line[2],
                    'loewdin_charge': line[3]
                })

    def _read_gross_populations(self, filename):

        with open(filename, 'r') as gross_pop_file:
            gross_pop_file.readline()
            gross_pop_file.readline()
            gross_pop_file.readline()
            while True:
                line = gross_pop_file.readline().split()
                if len(line) == 0:
                    break
                this_populations = {
                    'element': line[1],
                    'gross_populations': []
                }
                while True:
                    line = gross_pop_file.readline().split()
                    if len(line) == 0:
                        self.gross_populations.append(this_populations)
                        break
                    this_populations['gross_populations'].append({
                        'atomic_orbital': line[0],
                        'mulliken_gross_pop': line[1],
                        'loewdin_gross_pop': line[2]
                    })
