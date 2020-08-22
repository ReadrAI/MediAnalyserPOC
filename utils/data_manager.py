"""
Util functions for mail reception and sending
"""

import os
import pickle


class DataManager:

    modulePath = None

    @classmethod
    def getModulePath(cls):
        if cls.modulePath is not None:
            return cls.modulePath
        else:
            for root, subdirs, files in os.walk(os.path.expanduser("~")):
                for sd in subdirs:
                    if sd == "MediAnalyserPOC":
                        cls.modulePath = root + os.sep + sd
                        return cls.modulePath

    @classmethod
    def setModel(cls, model, data):
        with open(cls.getModulePath() + os.sep + 'ml_models' + os.sep + model + '.pickle', 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def getModel(cls, model):
        with open(cls.getModulePath() + os.sep + 'ml_models' + os.sep + model + '.pickle', 'rb') as f:
            return pickle.load(f)
