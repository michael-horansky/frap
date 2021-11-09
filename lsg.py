"""

created on: 2021-11-08
author:     michal horansky
----------------------------
classfile for the FRAP project
lsg: lindenmayer system generator
----------------------------
This software is distributed under the GNU General Public License (GPL-3.0-or-later).
It may be used, modified, shared, or built upon.
All derivative work must be distributed under the same license.

"""

from frap_functions import *


class lsg():
    
    # initializers and destructors
    def __init__(self, init_ruleset={}, init_default_axiom=''):
        self.ruleset = init_ruleset.copy()
        self.default_axiom = init_default_axiom
        
        
        
    # methods
    def get_rules(self):
        return(self.ruleset.copy())
    def set_rules(self, new_rules):
        self.ruleset = new_rules.copy()
        return(self)
    def add_rules(self, append_rules):
        for s_0, s_1 in append_rules.items():
            # if rule already exists, it will merely be updated
            self.ruleset[s_0] = s_1
        return(self)
    def delete_rule(self, obsolete_key):
        self.ruleset.pop(obsolete_key, None)
        return(self)
    def get_default_axiom(self):
        return(self.default_axiom)
    def set_default_axiom(self, new_default_axiom):
        self.default_axiom = new_default_axiom
        return(self)
    
    def iterate(self, depth, axiom = "__UNDEFINED__"):
        if axiom == "__UNDEFINED__":
            axiom = self.default_axiom
        if depth <= 0:
            return(axiom)
        new_lstring = ''
        max_rule_length = max_property(list(self.ruleset.values()), len)
        rule_keys = sorted(list(self.ruleset.keys()), key = lambda x : len(x), reverse = False )
        #print(rule_keys)
        index = 0
        while index < len(axiom):
            # We prioritize longer rules
            for substring_length in range(max_rule_length, -1, -1):
                if substring_length <= 0:
                    new_lstring += axiom[index]
                    index += 1
                    break
                if index + substring_length > len(axiom):
                    continue
                cur_substring = axiom[index:index + substring_length]
                if cur_substring in self.ruleset.keys():
                    new_lstring += self.ruleset[cur_substring]
                    index += substring_length
                    break
        return(self.iterate(depth - 1, new_lstring))
                    
    
    
    
