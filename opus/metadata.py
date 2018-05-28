# -*- coding: utf-8 -*-

class Metadata(object):
    def __init__(self, json):
        self.json = json
        self.set_general_constraints()

    def __repr__(self):
        return 'OPUS API Metadata Ring observation: {}'.format(self.ring_obs_id)

    @property
    def general_constraints(self):
        return self.json['General Constraints']

    def set_general_constraints(self):
        for key, value in self.general_constraints.items():
            if key == 'is_image':
                value = (value == 1)
            if value is not None and value != 'N/A':
                setattr(self, key, value)
