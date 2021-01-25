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
            cls.modulePath = os.getenv("REPOPATH")
            return cls.modulePath

    @classmethod
    def getModelPath(cls, model, tmp):
        return cls.getModulePath() + os.sep + 'ml_models' + ((os.sep + 'tmp') if tmp else '') + os.sep + model + '.pickle'

    @classmethod
    def setTmpModel(cls, model, data):
        with open(cls.getModelPath(model, True), 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def getTmpModel(cls, model):
        with open(cls.getModelPath(model, True), 'rb') as f:
            return pickle.load(f)

    @classmethod
    def getModel(cls, model):
        with open(cls.getModelPath(model, False), 'rb') as f:
            return pickle.load(f)

    @classmethod
    def validateModels(cls, models):
        for model in models:
            os.replace(cls.getModelPath(model, True), cls.getModelPath(model, False))
