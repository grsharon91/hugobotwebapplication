from abc import ABCMeta, abstractmethod
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import xgboost as xgb

class Model(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit(self, data, labels):
        pass

    @abstractmethod
    def predict(self, data):
        pass

    def getScore(self, type):
       pass

class ClassificationModel(Model):

    def __init__(self,model_name,params=None):
        self._m_name=model_name
        self._params=params
        self._model=None
        if self._m_name=='logreg':
            self._model=linear_model.LogisticRegression(C=1, penalty='l2', verbose =False,random_state=1)
        elif self._m_name=='rf':
            self._model =RandomForestClassifier(**params)
        elif self._m_name=='svm':
            self._model=svm.SVC(probability=True)
        elif self._m_name=='gb':
            self._model=GradientBoostingClassifier(**params)
        elif self._m_name == 'xgb':
            self._model =xgb.XGBClassifier(**params)
        elif self._m_name=='nb':
            self._model =MultinomialNB()


    def fit(self,data, labels):
        self._model.fit(data,labels)

    def predict(self, data):
        return  self._model.predict(data)

    def predict_proba(self, data):
        return self._model.predict_proba(data)[:,1]

    def getScore(self, y,pred,type=None):

        return metrics.roc_auc_score(y, pred)
        #return metrics.auc(roc_curve.fpr, roc_curve.tpr)
        # roc_curve = metrics.roc_curve(y_true=y,
        #y_score = pred,
        #drop_intermediate = True)
