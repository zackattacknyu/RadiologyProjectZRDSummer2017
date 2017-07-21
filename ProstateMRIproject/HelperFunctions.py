"""
This will convert from the excel column code, i.e. A, B, C ...
    AA, AB, ... , BA, BB, ...
to column number starting at index 0
"""
def getColumnNumber(letterCode):
    if(len(letterCode)<2):
        return getDistFromA(letterCode)
    else:
        firstDigitNum = (getDistFromA(letterCode[0])+1)
        return firstDigitNum*26 + (getDistFromA(letterCode[1]))

def getDistFromA(curLetter):
    return ord(curLetter)-ord('A')

