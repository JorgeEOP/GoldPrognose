import pandas as pd
from pandas import DataFrame as df

class DataFormatter:
    data = None
    dataAsDataFrame = None
    def __init__(self, data: str):
        """
        data is a string to the csv data
        """
        if (data != None):
            print ("DataFormatter: Data registered")
            self.data = data
        else:
            print ("DataFormatter::Warning, no data Provided")

    """Returns DataFrame"""
    def getDataAsDataFrame(self):
        if (self.data != None):
            df = pd.read_csv(self.data, parse_dates = [0])
            return df
    
    def setFormattedDataFrame(self):
        if (self.data != None):
            df = self.getDataAsDataFrame()
            df.set_index('Date', inplace=True)
            self.dataAsDataFrame = df
        
    def getFormattedDataFrame(self):
        return self.dataAsDataFrame
    
    @staticmethod
    def getDataBetweenDates(data: df, initialDate: str, endDate: str) -> df:
        """
        getDataBetweenDates: gets the dates between two dates
        """
        #data[formattedData.index > pd.to_datetime("2019-04-01")]
        return data.loc[initialDate : endDate]