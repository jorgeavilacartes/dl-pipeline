from sklearn.metrics import confusion_matrix as conf_matrix
from typing import List, Union

class Metrics:
    __slots__ = ["metrics"]
    def __init__(self, metrics: List[str] = ["accuracy","sensitivity","specificity","precision","neg-rate","f1-score"]):
        self.metrics = metrics

    def __call__(self, 
                    y_true: List[Union[int,str]], 
                    y_pred: List[Union[int,str]]
                    ):
        """return desired metrics"""
        dict_metrics = self.__get_metrics(y_true, y_pred)
        return {metric: dict_metrics.get(metric) for metric in self.metrics}

    def __get_metrics(self, y_true, y_pred):
        """Get all calculus to get metrics"""
        cm = conf_matrix(y_true, y_pred, labels=None, sample_weight=None)

        # Specificity, Sensitivity and Accuracy
        TN, FP, FN, TP = cm.ravel()

        # Accuracy
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        # Sensitivity/Recall 
        sensitivity = TP / (TP + FN)  
        # Specificity SP
        specificity = TN / (TN + FP)
        # Precision
        precision = TP / (TP + FP)
        # Negative Rate
        neg_rate = TN / (TN + FN)
        # F1-score
        f1_score = 2*(precision*sensitivity)/(precision+sensitivity)

        return {"accuracy": accuracy, "sensitivity": sensitivity, "specificity": specificity, "precision": precision, "neg-rate": neg_rate,"f1-score": f1_score}


    def __repr__(self,):
        """Print how class was initialized"""
        return f"MonitorValues({self.metrics!r})"