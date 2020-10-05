import os
import cv2
import time
import numpy as np

from collections import namedtuple
from typing import List, Optional,NamedTuple
from pydantic import BaseModel

class SummarizeScanner:

    def summarize(self, list_scanner: List[NamedTuple]):
        pass

    def plot_metric(self, metric: str, list_scanner: List[NamedTuple]):
        pass

    def __plot_mean(self,):
        pass
    
    def __plot_std(self,):
        pass

    def __plot_min(self,):
        pass

    def __plot_max(self,):
        pass

    def __plot_median(self,):
        pass

    def __plot_shape(self,):
        pass

class ImageScanner(SummarizeScanner):
    #__slots__ = ["metrics","list_scanner","ImgStats","axis","n_calls"]
    def __init__(self, 
        metrics: List[str] = ["img_id","shape","min","mean","std","max","median"],
        on_axis: int = 2
        ):
        # Metrics to scann
        self.metrics = metrics
        self.metrics.insert(0,"timestamp") if "timestamp" not in self.metrics else None
        
        # namedtuple to save stats
        self.list_scanner = []
        self.ImgStats = namedtuple("ImgStats", metrics)
        self.axis = tuple(channel for channel in range(3) if channel != on_axis)
        
        # count number of calls
        self.n_calls = 0
        

    def _mean(self, array_img):
        """Get mean of the image"""
        return np.mean(array_img, self.axis)
    
    def _std(self, array_img):
        """Get std of the image"""
        return np.std(array_img, self.axis)

    def _min(self, array_img):
        """Get min of the image"""
        return np.min(array_img, self.axis)

    def _max(self, array_img):
        """Get max of the image"""
        return np.max(array_img, self.axis)

    def _median(self, array_img):
        """Get median of the image"""
        return np.median(array_img, self.axis)

    def _shape(self, array_img):
        """Get shape of the image"""
        return array_img.shape
    
    def __count_calls(self,):
        """Number of calls"""
        self.n_calls += 1

    def __load_img(self, path_img: str):
        """Load image if exists"""
        if os.path.exists(path_img):
            img = cv2.imread(path_img)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return img
        else:
            raise Exception("File does not exists")
        
    def __getitem__(self, number):
        """Get the number-esim monitored value"""
        return self.list_scanner[int(number)]

    def __len__(self,):
        """Get number of scanned images"""
        return len(self.list_scanner)

    def __call__(self, 
        path_img: Optional[str] = None,
        array_img = None,
        return_metrics: bool = False
        ):
        """Get metrics of one image. Results are saved internally in atrribute 'list_scanner' """
        # If not array is provided, load the image
        if array_img is None:
            array_img = self.__load_img(path_img)
        
        # id to reference the image
        img_id = path_img if path_img else str(self.n_calls).zfill(6)
        metrics_res = [img_id]

        for metric in self.metrics:
            if metric == "mean":
                metrics_res.append(self._mean(array_img))
            if metric == "std":
                metrics_res.append(self._std(array_img))
            if metric == "min":
                metrics_res.append(self._min(array_img))
            if metric == "max":
                metrics_res.append(self._max(array_img))
            if metric == "median":
                metrics_res.append(self._median(array_img))
            if metric == "shape":
                metrics_res.append(self._shape(array_img))

        
        metrics_res.insert(0, self._get_localtime()) # add timestamp
        img_metrics = self.ImgStats._make(metrics_res)
        self.list_scanner.append(img_metrics)
        self.__count_calls()

        if return_metrics:
            return img_metrics

    def _get_localtime(self,):
        """Get a string representation of current time 
        <DayName> <Month> <NumberDay> hh:mm:ss <Year>"""
        return time.asctime(time.localtime(time.time()))
