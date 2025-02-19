#Plot Both dataSets
def getMaxPrice(firstPrice: float, secondPrice: float) -> float:
    if (firstPrice > secondPrice):
        return firstPrice
    elif (firstPrice < secondPrice):
        return secondPrice
