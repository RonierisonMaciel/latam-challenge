"""
Flight Delay Prediction
Author: Ronierison Maciel
Date: 2023-10-06
"""

from datetime import datetime
import warnings
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from typing import Tuple, Union, List
warnings.filterwarnings('ignore')


class DelayModel:
    THRESHOLD_MINUTES = 10

    def __init__(self):
        warnings.filterwarnings('ignore')
        self._model = None
        self.top_10_features = [
            "OPERA_Latin American Wings",
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        self.airlines = None

    @staticmethod
    def _get_period_day(date: str) -> str:
        time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        periods = {
            "morning": (datetime.strptime("05:00", '%H:%M').time(), datetime.strptime("11:59", '%H:%M').time()),
            "afternoon": (datetime.strptime("12:00", '%H:%M').time(), datetime.strptime("18:59", '%H:%M').time()),
            "evening": (datetime.strptime("19:00", '%H:%M').time(), datetime.strptime("23:59", '%H:%M').time()),
            "night": (datetime.strptime("00:00", '%H:%M').time(), datetime.strptime("4:59", '%H:%M').time())
        }
        
        for period, (start, end) in periods.items():
            if start <= time <= end:
                return period

    @staticmethod
    def _is_high_season(date: str) -> int:
        fecha = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        year = fecha.year
        high_season_ranges = [
            (datetime.strptime('15-Dec', '%d-%b').replace(year=year), datetime.strptime('31-Dec', '%d-%b').replace(year=year)),
            (datetime.strptime('1-Jan', '%d-%b').replace(year=year), datetime.strptime('3-Mar', '%d-%b').replace(year=year)),
            (datetime.strptime('15-Jul', '%d-%b').replace(year=year), datetime.strptime('31-Jul', '%d-%b').replace(year=year)),
            (datetime.strptime('11-Sep', '%d-%b').replace(year=year), datetime.strptime('30-Sep', '%d-%b').replace(year=year))
        ]

        return int(any(start <= fecha <= end for start, end in high_season_ranges))

    @staticmethod
    def _get_min_diff(row: pd.Series) -> float:
        fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        return (fecha_o - fecha_i).total_seconds() / 60

    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        self.airlines = data['OPERA'].unique()
        
        data['period_day'] = data['Fecha-I'].apply(self._get_period_day)
        data['high_season'] = data['Fecha-I'].apply(self._is_high_season)
        data['min_diff'] = data.apply(self._get_min_diff, axis=1)
        data['delay'] = np.where(data['min_diff'] > self.THRESHOLD_MINUTES, 1, 0)

        features = pd.concat([
            pd.get_dummies(data[column], prefix=column) for column in ['OPERA', 'TIPOVUELO', 'MES']
        ], axis=1)
        
        features = features[self.top_10_features]
        
        return (features, data[['delay']]) if target_column else features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        x_train, _, y_train, _ = train_test_split(features, target, test_size=0.33, random_state=42)
        class_weights = {1: len(y_train[y_train == 0]) / len(y_train), 0: len(y_train[y_train == 1]) / len(y_train)}
        
        self._model = LogisticRegression(class_weight=class_weights)
        self._model.fit(x_train, y_train.values.ravel())

    def predict(self, features: pd.DataFrame) -> List[int]:
        return self._model.predict(features).tolist()
