# Seed
import random
random.seed(2)

from collections import namedtuple
from collections import Counter
from typing import List, Union, Optional, Tuple
from sklearn.model_selection import train_test_split

class DataSelector:

    def __init__(self,
                    id_labels: List[Union[str,int]], 
                    labels: List[Union[str,int]],
                ):
        self._id = range(len(labels))
        self.id_labels  = id_labels
        self.labels = labels
        self.datasets = {}

    def __call__(self, 
                    print_summary: bool = True,
                    balanced_on: Optional[List[Union[str,int]]] = None,
                    train_size: float = 0.7,
                    test_size: float = None
                    ):
        print("Generating train, validation and test sets...")
        self.train_val_test_split(train_size, test_size, balanced_on)
        print("Datasets successfully generated. See 'datasets' attribute.")
        print(self.get_summary_labels()) if print_summary else None


    def train_val_test_split(self, 
                                train_size: float, 
                                test_size: Optional[float], 
                                balanced_on: List[Union[str,int]],
                                exclusive_by = List[Union[str,int]],
                            ):
        X_dataset = self.id_labels if self.id_labels else self._id
        X = self._id
        y = self.labels
        test_size = test_size if test_size else (1 - train_size) / 2
        
        # train+val and test sets
        X_train_val, X_test, y_train_val, y_test = self.__split_dataset(X, y, test_size, balanced_on)
        # split train and val
        balanced_on = y_train_val if balanced_on else None
        X_train, X_val, y_train, y_val = self.__split_dataset(X_train_val, y_train_val, test_size / (1-test_size), balanced_on)

        self.datasets = {           
            "X_train": [X_dataset[idx] for idx in X_train], 
            "X_val"  : [X_dataset[idx] for idx in X_val],
            "X_test" : [X_dataset[idx] for idx in X_test], 
            "y_train": y_train, 
            "y_val"  : y_val,
            "y_test" : y_test
            }
        
        self._id_datasets = {
            "train": [self._id[idx] for idx in X_train],
            "val": [self._id[idx] for idx in X_val],
            "test": [self._id[idx] for idx in X_test]
        }

    def get_summary_labels(self,):
        """Count frequency of labels in each dataset"""
        return {ds: self.__count_labels_on_dataset(self.datasets.get("y_"+ ds)) 
                    for ds in ["train","val","test"]
                }

    def __split_dataset(self, 
                            X: List[Optional[Union[str,int]]], 
                            y: List[Optional[Union[str,int]]], 
                            perc: float, 
                            balanced_on: List[Optional[Union[str,int]]] = None
                        ) -> Tuple:
        """split one dataset in 2 independent datasets"""
        X1, X2, y1, y2 = train_test_split(X, y, 
                                        test_size = perc, 
                                        stratify=balanced_on
                                        )
        return X1, X2, y1, y2

    def __count_labels_on_dataset(self, labels: List[Union[int,str]]):
        return dict(Counter(labels))

    def __reorder_datasets(self,):
        pass
    
    def __datasets_mutually_exclusive(self,):
        pass
    

