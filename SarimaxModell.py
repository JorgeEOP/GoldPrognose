from pandas import DataFrame
import matplotlib.pyplot as plt


from statsmodels.tsa.statespace.sarimax import SARIMAX

'''
Funkionen um das Modell Sarimax für Zeitreihen Daten zu analysieren
'''

seasonalOrderDict = {
    'AROrder': 'P',
    'IntegrationOrder': 'D',
    'MAOrder': 'Q',
    'Periodicity': 's'
}

ROOT_PLOT_PATH = "Grafiken/"

def simpleSarimaxForecast(trainingSet: DataFrame, testSet: DataFrame) -> DataFrame:
    SARIMAXModel = SARIMAX(trainingSet, order = (1, 1, 5), seasonal_order = (2, 2, 3, 12))
    SARIMAXModel = SARIMAXModel.fit()

    yForecast = SARIMAXModel.get_forecast( len(testSet.index) )
    forecastDF = yForecast.conf_int(alpha = 0.05) 

    forecastDF["Predictions"] = SARIMAXModel.predict(start = forecastDF.index[0], end = forecastDF.index[-1])
    forecastDF.index = testSet.index
    forecastDF = forecastDF["Predictions"]
    return forecastDF

def getSeasonalParameterVariationAsVideo(parameterToVary: str, parameterVariation: int, trainingSet: DataFrame, testSet: DataFrame) -> None:
    '''
    parameterToVary: in the SARIMAX model. It can be 'P', 'D', 'Q', 's'
    '''
    print ("TRAINING_SET:\n", trainingSet)
    trainingSet.head()

    print ('-----------------')
    seasonalOrder = (1, 2, 3, 12)
    for i in range(parameterVariation):
        print("getParameterVariationAsVideo:: Predicting best values iteration: ", i)

        newSeasonalOrder = getSeasonalOrderTuple(seasonalOrder, parameterToVary, i)
        print("getParameterVariationAsVideo:: new Seasonal order: ", newSeasonalOrder)

        #SARIMAXModel = SARIMAX(y, order = (1, 1, 5), seasonal_order=(1, 2, 3, 12))
        SARIMAXModel = SARIMAX(trainingSet, order = (1, 1, 5), seasonal_order = newSeasonalOrder)
        SARIMAXModel = SARIMAXModel.fit()

        yForecast = SARIMAXModel.get_forecast( len(testSet.index) )
        forecastDF = yForecast.conf_int(alpha = 0.05) 

        forecastDF["Predictions"] = SARIMAXModel.predict(start = forecastDF.index[0], end = forecastDF.index[-1])
        forecastDF.index = testSet.index
        forecastDF = forecastDF["Predictions"]

        plt.ylabel('Dollars (\u0024)')
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.title("Dollar Kurs Daten")
        plt.ylim(900, 3500)
        plt.plot(trainingSet.index, trainingSet["Price"], color = "black", label = "Train Dataset")
        plt.plot(testSet.index, testSet["Price"], color = "red", label = "Test Dataset")
        plt.plot(forecastDF, color='green', label = 'Predictions: ' + '(' + str(i) + ', 2, 3, 12)')
        plt.legend(loc='upper left')
        plt.savefig(ROOT_PLOT_PATH + "GoldKurs" + str(i) + ".png")
        plt.clf()
        # Produce a small animation of the dollar course

def getSeasonalOrderTuple(sarimaxTuple: tuple, sarimaxParameterToChange: str, value: int) -> tuple:
    '''
    @sarimaxTuple: (P,D,Q,s)
    @sarimaxParameterToChange: 'P' or 'D' or 'Q' or 's'
    @value: value to assign to the SARIMAX parameter
    '''
    sarimaxAsList = list(sarimaxTuple)
    match sarimaxParameterToChange:
        case 'P':
            sarimaxAsList[0] = value
        case 'D':
            sarimaxAsList[1] = value
        case 'Q':
            sarimaxAsList[2] = value
        case 's':
            sarimaxAsList[3] = value
    return tuple(sarimaxAsList)