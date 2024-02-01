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
    bw5_1 = np.array(getData(8 ,    "logs/EC2/logs_8_180_rampUp/logs/c"))
    bw10_1 = np.array(getData(16,   "logs/EC2/logs_16_180_rampUp/logs/c"))
    bw25_1 = np.array(getData(32,   "logs/EC2/logs_32_180_rampUp/logs/c"))
    bw50_1 = np.array(getData(64,   "logs/EC2/logs_64_180_rampUp/logs/c"))
    bw100_1 = np.array(getData(128, "logs/EC2/logs_128_180_rampUp/logs/c"))
    bwws_1 = np.array(getData(20, "logs/RampUp/Cadvise/cadvise_rampUp"))
    br_1 = np.array(getBitrates("netTraces/rampUp.json"))
    data5_1 = np.array(getVariance(bw5_1, br_1))
    data10_1 = np.array(getVariance(bw10_1, br_1))
    data25_1 = np.array(getVariance(bw25_1, br_1))
    data50_1 = np.array(getVariance(bw50_1, br_1))
    data100_1 = np.array(getVariance(bw100_1, br_1))
    dataws_1 = np.array(getVariance(bwws_1, br_1))

    # Second Set
    bw5_2 = np.array(getData(8 ,    "logs/EC2/logs_8_180_rampDown/logs/c"))
    bw10_2 = np.array(getData(16,   "logs/EC2/logs_16_180_rampDown/logs/c"))
    bw25_2 = np.array(getData(32,   "logs/EC2/logs_32_180_rampDown/logs/c"))
    bw50_2 = np.array(getData(64,   "logs/EC2/logs_64_180_rampDown/logs/c"))
    bw100_2 = np.array(getData(128, "logs/EC2/logs_128_180_rampDown/logs/c"))
    bwws_2 = np.array(getData(20, "logs/RampDown/Cadvise/cadvise_rampDown"))
    br_2 = np.array(getBitrates("netTraces/rampDown.json"))
    data5_2 = np.array(getVariance(bw5_2, br_2))
    data10_2 = np.array(getVariance(bw10_2, br_2))
    data25_2 = np.array(getVariance(bw25_2, br_2))
    data50_2 = np.array(getVariance(bw50_2, br_2))
    data100_2 = np.array(getVariance(bw100_2, br_2))
    dataws_2 = np.array(getVariance(bwws_2, br_2))


    # Third Set
    bw5_3 = np.array(getData(8 ,    "logs/EC2/logs_8_180_cascade/logs/c"))
    bw10_3 = np.array(getData(16,   "logs/EC2/logs_16_180_cascade/logs/c"))
    bw25_3 = np.array(getData(32,   "logs/EC2/logs_32_180_cascade/logs/c"))
    bw50_3 = np.array(getData(64,   "logs/EC2/logs_64_180_cascade/logs/c"))
    bw100_3 = np.array(getData(128, "logs/EC2/logs_128_180_cascade/logs/c"))
    bwws_3 = np.array(getData(20, "logs/Cascade/Cadvise/cadvise_cascade"))
    br_3 = np.array(getBitrates("netTraces/Cascade.json"))
    data5_3 = np.array(getVariance(bw5_3, br_3))
    data10_3 = np.array(getVariance(bw10_3, br_3))
    data25_3 = np.array(getVariance(bw25_3, br_3))
    data50_3 = np.array(getVariance(bw50_3, br_3))
    data100_3 = np.array(getVariance(bw100_3, br_3))
    dataws_3 = np.array(getVariance(bwws_3, br_3))

    # Fourth Set
    bw5_4 = np.array(getData(8 ,    "logs/EC2/logs_8_180_steps/logs/c"))
    bw10_4 = np.array(getData(16,   "logs/EC2/logs_16_180_steps/logs/c"))
    bw25_4 = np.array(getData(32,   "logs/EC2/logs_32_180_steps/logs/c"))
    bw50_4 = np.array(getData(64,   "logs/EC2/logs_64_180_steps/logs/c"))
    bw100_4 = np.array(getData(128, "logs/EC2/logs_128_180_steps/logs/c"))
    bwws_4 = np.array(getData(20, "logs/Steps/Cadvise/cadvise_steps"))

    br_4 = np.array(getBitrates("netTraces/steps.json"))
    data5_4 = np.array(getVariance(bw5_4, br_4))
    data10_4 = np.array(getVariance(bw10_4, br_4))
    data25_4 = np.array(getVariance(bw25_4, br_4))
    data50_4 = np.array(getVariance(bw50_4, br_4))
    data100_4 = np.array(getVariance(bw100_4, br_4))
    dataws_4 = np.array(getVariance(bwws_4, br_4))
    # Fifth Set
    bw5_5 = np.array(getData(8 ,    "logs/EC2/logs_8_180_stable/logs/c"))
    bw10_5 = np.array(getData(16,   "logs/EC2/logs_16_180_stable/logs/c"))
    bw25_5 = np.array(getData(32,   "logs/EC2/logs_32_180_stable/logs/c"))
    bw50_5 = np.array(getData(64,   "logs/EC2/logs_64_180_stable/logs/c"))
    bw100_5 = np.array(getData(128, "logs/EC2/logs_128_180_stable/logs/c"))
    bwws_5 = np.array(getData(20, "logs/Stable/Cadvise/cadvise_stable"))
    br_5 = np.array(getBitrates("netTraces/stable.json"))
    data5_5 = np.array(getVariance(bw5_5, br_5))
    data10_5 = np.array(getVariance(bw10_5, br_5))
    data25_5 = np.array(getVariance(bw25_5, br_5))
    data50_5 = np.array(getVariance(bw50_5, br_5))
    data100_5 = np.array(getVariance(bw100_5, br_5))
    dataws_5 = np.array(getVariance(bwws_5, br_5))

    print("Mean Variances: ")
    print("Ramp Up")
    print(f'PyStream = [8: {np.mean(data5_1)}, 16: {np.mean(data10_1)}, 32: {np.mean(data25_1)}, 64: {np.mean(data50_1)}, 128: { np.mean(data100_1)}]')
    print(f'Cadvise = [20: {np.mean(dataws_1)}]')
    print("Ramp Down")
    print(f'PyStream = [8: {np.mean(data5_2)}, 16: {np.mean(data10_2)}, 32: {np.mean(data25_2)}, 64: {np.mean(data50_2)}, 128: { np.mean(data100_2)}]')
    print(f'Cadvise = [20: {np.mean(dataws_2)}]')
    print("Cascade")
    print(f'PyStream = [8: {np.mean(data5_3)}, 16: {np.mean(data10_3)}, 32: {np.mean(data25_3)}, 64: {np.mean(data50_3)}, 128: { np.mean(data100_3)}]')
    print(f'Cadvise = [20: {np.mean(dataws_3)}]')
    print("Steps")
    print(f'PyStream = [8: {np.mean(data5_4)}, 16: {np.mean(data10_4)}, 32: {np.mean(data25_4)}, 64: {np.mean(data50_4)}, 128: { np.mean(data100_4)}]')
    print(f'Cadvise = [20: {np.mean(dataws_4)}]')
    print("Stable")
    print(f'PyStream = [8: {np.mean(data5_5)}, 16: {np.mean(data10_5)}, 32: {np.mean(data25_5)}, 64: {np.mean(data50_5)}, 128: { np.mean(data100_5)}]')
    print(f'Cadvise = [20: {np.mean(dataws_5)}]')



    fig = plt.figure(figsize=(30, 5))
    ax1 = plt.subplot2grid((6, 125), (0, 0), colspan=20, rowspan=5)
    plt.yscale('log')
    ax1.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax1.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax1.set_title('Ramp Up',fontsize=15)

    ax2 = plt.subplot2grid((6, 125), (0, 25), colspan=20, rowspan=5)
    plt.yscale('log')
    ax2.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax2.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax2.set_title('Ramp Down',fontsize=15)

    ax3 = plt.subplot2grid((6, 125), (0, 50), colspan=20, rowspan=5)
    plt.yscale('log')
    ax3.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax3.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax3.set_title('Cascade',fontsize=15)

    ax4 = plt.subplot2grid((6, 125), (0, 75), colspan=20, rowspan=5)
    plt.yscale('log')
    ax4.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax4.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax4.set_title('Steps',fontsize=15)

    ax5 = plt.subplot2grid((6, 125), (0, 100), colspan=20, rowspan=5)
    plt.yscale('log')
    ax5.set_ylabel('Deviation from Real Bitrate (kbps)',fontsize=13)
    ax5.set_xlabel('Number of Concurrent Clients',fontsize=13)
    ax5.set_title('Stable',fontsize=15)

    
    data_1 = [data5_1, data10_1, data25_1, data50_1, data100_1]
    data_2 = [data5_2, data10_2, data25_2, data50_2, data100_2]
    data_3 = [data5_3, data10_3, data25_3, data50_3, data100_3]
    data_4 = [data5_4, data10_4, data25_4, data50_4, data100_4]
    data_5 = [data5_5, data10_5, data25_5, data50_5, data100_5]

    # Create a boxplot
    ax1.boxplot(data_1,labels=['8', '16', '32', '64', '128'])
    ax2.boxplot(data_2,labels=['8', '16', '32', '64', '128'])
    ax3.boxplot(data_3,labels=['8', '16', '32', '64', '128'])
    ax4.boxplot(data_4,labels=['8', '16', '32', '64', '128'])
    ax5.boxplot(data_5,labels=['8', '16', '32', '64', '128'])

    # First Set
    er5_1 = [getMeanError(bw5_1, br_1)]
    er10_1 = [getMeanError(bw10_1, br_1)]
    er25_1 = [getMeanError(bw25_1, br_1)]
    er50_1 = [getMeanError(bw50_1, br_1)]
    err100_1 = [getMeanError(bw100_1, br_1)]

    # Second Set
    er5_2 = [getMeanError(bw5_2, br_2)]
    er10_2 = [getMeanError(bw10_2, br_2)]
    er25_2 = [getMeanError(bw25_2, br_2)]
    er50_2 = [getMeanError(bw50_2, br_2)]
    err100_2 = [getMeanError(bw100_2, br_2)]

    # Third Set
    er5_3 = [getMeanError(bw5_3, br_3)]
    er10_3 = [getMeanError(bw10_3, br_3)]
    er25_3 = [getMeanError(bw25_3, br_3)]
    er50_3 = [getMeanError(bw50_3, br_3)]
    err100_3 = [getMeanError(bw100_3, br_3)]

    # Fourth Set
    er5_4 = [getMeanError(bw5_4, br_4)]
    er10_4 = [getMeanError(bw10_4, br_4)]
    er25_4 = [getMeanError(bw25_4, br_4)]
    er50_4 = [getMeanError(bw50_4, br_4)]
    err100_4 = [getMeanError(bw100_4, br_4)]

    # Fifth Set
    er5_5 = [getMeanError(bw5_5, br_5)]
    er10_5 = [getMeanError(bw10_5, br_5)]
    er25_5 = [getMeanError(bw25_5, br_5)]
    er50_5 = [getMeanError(bw50_5, br_5)]
    err100_5 = [getMeanError(bw100_5, br_5)]

    # Prepare data for plotting
    var_1 = [er5_1, er10_1, er25_1, er50_1, err100_1]
    var_2 = [er5_2, er10_2, er25_2, er50_2, err100_2]
    var_3 = [er5_3, er10_3, er25_3, er50_3, err100_3]
    var_4 = [er5_4, er10_4, er25_4, er50_4, err100_4]
    var_5 = [er5_5, er10_5, er25_5, er50_5, err100_5]

    # Plotting
    ax1.plot([1, 2, 3, 4, 5], var_1, ':', color='red', marker='o')
    ax2.plot([1, 2, 3, 4, 5], var_2, ':', color='red', marker='o')
    ax3.plot([1, 2, 3, 4, 5], var_3, ':', color='red', marker='o')
    ax4.plot([1, 2, 3, 4, 5], var_4, ':', color='red', marker='o')
    ax5.plot([1, 2, 3, 4, 5], var_5, ':', color='red', marker='o')
    
    plt.tight_layout()
    plt.savefig("Figures/loadPlot.png")
    plt.show()

