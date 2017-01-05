class LogPhase(object):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.op_ve = {}
        self.strategy = {}

#        self.feasibility = feasiblity
#        self.matching = matching
#        self.v&e&p_selected = {}
#        self.schedule = {}
#        self.time = {}
#        self.cost = {}
#        self.environmental = environment
#        self.risk = risk


class DefPhase(object):

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.op_seq_prep = []  # includes all individual logistic operations
        self.op_seq_sea = {}
        self.op_seq_demob = []
        self.ve_combination = {}
        self.sol = {}
        self.sol_cost = {}


class VE_solutions(object):

    def __init__(self, id):
        self.id = id
        self.sol_combi = {}
        self.sol_ves = {}
        self.sol_eq = {}
        self.schedule = {}
        self.cost = {}
