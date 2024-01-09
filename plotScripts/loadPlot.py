import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import operator
import numpy as np
import sys, json, re

data = list()
stalls = list()

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

#Find the stall data in the log file and process it, splitting into bandwidth, buffer and latency
#@param numIt: number of iterations i.e. number of log files
#@param file: log file name
def getData(numIt, file):
    global stalls
    data = [0] * 120
    if numIt == 1:
        stalls = lines_that_contain("stall", open(file+".log", "r"))[0].split("\"",1)[1].split("source",1)[0][:-3]
        stalls = stalls.replace("null", "0")
        stalls = stalls.replace("\"", "")
        tokens = stalls.split("availibleBW")
        stalls = re.findall(r'\[(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)\]', tokens[0])
        tokens = tokens[1].split("currentBuffer")
        availableBW = list(map(float,re.findall(r'\d+',tokens[0])))
        tokens = tokens[1].split("currentLatency")
        availableBuffer = list(map(float, re.findall(r'\d+\.*\d*',tokens[0])))
        availableLatency = list(map(float, re.findall(r'\d+\.*\d*',tokens[1])))

        data = availableBW
        # print(data)
        return data[:119]
    for i in range(1, numIt+1):
        try:
            stalls = lines_that_contain("stall", open(file+str(i)+".log", "r"))[0].split("\"",1)[1].split("source",1)[0][:-3]
            stalls = stalls.replace("null", "0")
            stalls = stalls.replace("\"", "")
            tokens = stalls.split("availibleBW")
            stalls = re.findall(r'\[(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)\]', tokens[0])
            tokens = tokens[1].split("currentBuffer")
            availableBW = list(map(float,re.findall(r'\d+',tokens[0])))
            tokens = tokens[1].split("currentLatency")
            availableBuffer = list(map(float, re.findall(r'\d+\.*\d*',tokens[0])))
            availableLatency = list(map(float, re.findall(r'\d+\.*\d*',tokens[1])))
        except:
            availableBW = [0] * 119

        data = [a+b for a,b in zip(data, availableBW)]
        # print(data)

    data[:] = [x / numIt for x in data]
    # print(data)
    return data

def getBitrates(jsonFile):
    dataRates = []
    with(open(jsonFile) as jsonData):
        data = json.load(jsonData)
    for i in data:
        for j in range(0, i["duration"]):
            dataRates.append(int(i["clientIngress"]))
    return dataRates[:119]

def getMeanError(bw, br):
    error = [abs(a-b) for a,b in zip(bw, br)]
    return sum(error)/len(error)


def getVariance(bw, br):
    variance = []
    for i in range(len(bw)):
        diff = abs(bw[i] - br[i])
        variance.append(diff)
    return variance
    


if __name__ == "__main__":

    #This would be easier with args...

    bw5 = np.array(getData(5, "logs/Stable/load_5_stable"))
    bw10 = np.array(getData(10, "logs/Stable/load_10_stable"))
    bw25 = np.array(getData(25, "logs/Stable/load_25_stable"))
    bw50 = np.array(getData(50, "logs/Stable/load_50_stable"))

    br = np.array(getBitrates("netTraces/stable.json"))
    data5 = np.array(getVariance(bw5, br))
    data10 = np.array(getVariance(bw10, br))
    data25 = np.array(getVariance(bw25, br))
    data50 = np.array(getVariance(bw50, br))

    # Combine data into a list
    data = [data5, data10, data25, data50]

    # Create a boxplot
    plt.boxplot(data, labels=['5', '10', '25', '50'])
    plt.xlabel('Number of Iterations')
    plt.ylabel('Deviation from Real Bitrate (kbps)')
    plt.title('Stable')

    er5=[getMeanError(bw5, br)]
    er10=[getMeanError(bw10, br)]
    er25=[getMeanError(bw25, br)]
    er50=[getMeanError(bw50, br)]

    var=[er5, er10, er25, er50]
    plt.plot([1, 2, 3, 4], var,':',color='red',marker='o')

    # Show the plot
    plt.savefig('Figures/boxplot_stable.png')
    plt.show()
