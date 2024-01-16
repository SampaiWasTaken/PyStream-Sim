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

    # First Set
    bw5_1 = np.array(getData(5 ,  "logs/rampUp/load_5_rampUp"))
    bw10_1 = np.array(getData(10, "logs/rampUp/load_10_rampUp"))
    bw25_1 = np.array(getData(25, "logs/rampUp/load_25_rampUp"))
    bw50_1 = np.array(getData(50, "logs/rampUp/load_50_raampUp"))
    br_1 = np.array(getBitrates("netTraces/rampUp.json"))
    data5_1 = np.array(getVariance(bw5_1, br_1))
    data10_1 = np.array(getVariance(bw10_1, br_1))
    data25_1 = np.array(getVariance(bw25_1, br_1))
    data50_1 = np.array(getVariance(bw50_1, br_1))

    # Second Set
    bw5_2 = np.array(getData(5,   "logs/rampDown/load_5_rampDown"))
    bw10_2 = np.array(getData(10, "logs/rampDown/load_10_rampDown"))
    bw25_2 = np.array(getData(25, "logs/rampDown/load_25_rampDown"))
    bw50_2 = np.array(getData(50, "logs/rampDown/load_50_rampDown"))
    br_2 = np.array(getBitrates("netTraces/rampDown.json"))
    data5_2 = np.array(getVariance(bw5_2, br_2))
    data10_2 = np.array(getVariance(bw10_2, br_2))
    data25_2 = np.array(getVariance(bw25_2, br_2))
    data50_2 = np.array(getVariance(bw50_2, br_2))

    # Third Set
    bw5_3 = np.array(getData(5,   "logs/Cascade/load_5_cascade"))
    bw10_3 = np.array(getData(10, "logs/Cascade/load_10_cascade"))
    bw25_3 = np.array(getData(25, "logs/Cascade/load_25_cascade"))
    bw50_3 = np.array(getData(50, "logs/Cascade/load_50_cascade"))
    br_3 = np.array(getBitrates("netTraces/Cascade.json"))
    data5_3 = np.array(getVariance(bw5_3, br_3))
    data10_3 = np.array(getVariance(bw10_3, br_3))
    data25_3 = np.array(getVariance(bw25_3, br_3))
    data50_3 = np.array(getVariance(bw50_3, br_3))

    # Fourth Set
    bw5_4 = np.array(getData(5,   "logs/Steps/load_5_steps"))
    bw10_4 = np.array(getData(10, "logs/Steps/load_10_steps"))
    bw25_4 = np.array(getData(25, "logs/Steps/load_25_steps"))
    bw50_4 = np.array(getData(50, "logs/Steps/load_50_steps"))
    br_4 = np.array(getBitrates("netTraces/steps.json"))
    data5_4 = np.array(getVariance(bw5_4, br_4))
    data10_4 = np.array(getVariance(bw10_4, br_4))
    data25_4 = np.array(getVariance(bw25_4, br_4))
    data50_4 = np.array(getVariance(bw50_4, br_4))

    # Fifth Set
    bw5_5 = np.array(getData(5, "logs/Stable/load_5_stable"))
    bw10_5 = np.array(getData(10, "logs/Stable/load_10_stable"))
    bw25_5 = np.array(getData(25, "logs/Stable/load_25_stable"))
    bw50_5 = np.array(getData(50, "logs/Stable/load_50_stable"))
    br_5 = np.array(getBitrates("netTraces/stable.json"))
    data5_5 = np.array(getVariance(bw5_5, br_5))
    data10_5 = np.array(getVariance(bw10_5, br_5))
    data25_5 = np.array(getVariance(bw25_5, br_5))
    data50_5 = np.array(getVariance(bw50_5, br_5))



    fig = plt.figure(figsize=(30, 5))
    ax1 = plt.subplot2grid((6, 125), (0, 0), colspan=20, rowspan=5)
    ax1.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax1.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax1.set_title('Ramp Up',fontsize=15)

    ax2 = plt.subplot2grid((6, 125), (0, 25), colspan=20, rowspan=5)
    ax2.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax2.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax2.set_title('Ramp Down',fontsize=15)

    ax3 = plt.subplot2grid((6, 125), (0, 50), colspan=20, rowspan=5)
    ax3.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax3.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax3.set_title('Cascade',fontsize=15)

    ax4 = plt.subplot2grid((6, 125), (0, 75), colspan=20, rowspan=5)
    ax4.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax4.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax4.set_title('Steps',fontsize=15)

    ax5 = plt.subplot2grid((6, 125), (0, 100), colspan=20, rowspan=5)
    ax5.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax5.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax5.set_title('Stable',fontsize=15)

    
    data_1 = [data5_1, data10_1, data25_1, data50_1]
    data_2 = [data5_2, data10_2, data25_2, data50_2]
    data_3 = [data5_3, data10_3, data25_3, data50_3]
    data_4 = [data5_4, data10_4, data25_4, data50_4]
    data_5 = [data5_5, data10_5, data25_5, data50_5]

    # Create a boxplot
    ax1.boxplot(data_1)
    ax2.boxplot(data_2)
    ax3.boxplot(data_3)
    ax4.boxplot(data_4)
    ax5.boxplot(data_5)

    # First Set
    er5_1 = [getMeanError(bw5_1, br_1)]
    er10_1 = [getMeanError(bw10_1, br_1)]
    er25_1 = [getMeanError(bw25_1, br_1)]
    er50_1 = [getMeanError(bw50_1, br_1)]

    # Second Set
    er5_2 = [getMeanError(bw5_2, br_2)]
    er10_2 = [getMeanError(bw10_2, br_2)]
    er25_2 = [getMeanError(bw25_2, br_2)]
    er50_2 = [getMeanError(bw50_2, br_2)]

    # Third Set
    er5_3 = [getMeanError(bw5_3, br_3)]
    er10_3 = [getMeanError(bw10_3, br_3)]
    er25_3 = [getMeanError(bw25_3, br_3)]
    er50_3 = [getMeanError(bw50_3, br_3)]

    # Fourth Set
    er5_4 = [getMeanError(bw5_4, br_4)]
    er10_4 = [getMeanError(bw10_4, br_4)]
    er25_4 = [getMeanError(bw25_4, br_4)]
    er50_4 = [getMeanError(bw50_4, br_4)]

    # Fifth Set
    er5_5 = [getMeanError(bw5_5, br_5)]
    er10_5 = [getMeanError(bw10_5, br_5)]
    er25_5 = [getMeanError(bw25_5, br_5)]
    er50_5 = [getMeanError(bw50_5, br_5)]

    # Prepare data for plotting
    var_1 = [er5_1, er10_1, er25_1, er50_1]
    var_2 = [er5_2, er10_2, er25_2, er50_2]
    var_3 = [er5_3, er10_3, er25_3, er50_3]
    var_4 = [er5_4, er10_4, er25_4, er50_4]
    var_5 = [er5_5, er10_5, er25_5, er50_5]

    # Plotting
    ax1.plot([1, 2, 3, 4], var_1, ':', color='red', marker='o')
    ax2.plot([1, 2, 3, 4], var_2, ':', color='red', marker='o')
    ax3.plot([1, 2, 3, 4], var_3, ':', color='red', marker='o')
    ax4.plot([1, 2, 3, 4], var_4, ':', color='red', marker='o')
    ax5.plot([1, 2, 3, 4], var_5, ':', color='red', marker='o')
    
    plt.tight_layout()
    plt.savefig("loadPlot.png")
    plt.show()

