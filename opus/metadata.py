# -*- coding: utf-8 -*-

class Metadata(object):
    def __init__(self, json):
        self._json = json
        self.set_general_constraints()
        self.set_other_constraints()

    def __repr__(self):
        return 'OPUS API Metadata Ring observation: {}'.format(self.ring_obs_id)

    @property
    def general_constraints(self):
        return self._json['General Constraints']

    def set_general_constraints(self):
        '''Save the General Constraints parameter as attributs'''
        for key, value in self.general_constraints.items():
            if key == 'is_image':
                value = (value == 1)
            if value is not None and value != 'N/A':
                setattr(self, key, value)

    def set_other_constraints(self):
        '''Save other Constraints as sub-attributes'''
        for label, constraints in self._json.items():
            if label != 'General Constraints':
                key = label.lower().replace(' ', '_').replace('_constraints','')
                value = Constraints(constraints)
                setattr(self, key, value)


class Constraints(object):
    def __init__(self, constraints={}):
        for key, value in constraints.items():
            if value is not None and value != -999:
                setattr(self, key, value)

    def __repr__(self):
        return 'Metadata constraints'
