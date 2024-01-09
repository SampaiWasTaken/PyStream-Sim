import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import sys, json, re

data = list()
stalls = list()

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

def getData(file):
    global stalls
    stalls = lines_that_contain("stall", open(file, "r"))[0].split("\"",1)[1].split("source",1)[0][:-3]
    stalls = stalls.replace("null", "0")
    stalls = stalls.replace("\"", "")
    tokens = stalls.split("availibleBW")
    stalls = re.findall(r'\[(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)\]', tokens[0])
    tokens = tokens[1].split("currentBuffer")
    availableBW = list(map(float,re.findall(r'\d+',tokens[0])))
    tokens = tokens[1].split("currentLatency")
    availableBuffer = list(map(float, re.findall(r'\d+\.*\d*',tokens[0])))
    availableLatency = list(map(float, re.findall(r'\d+\.*\d*',tokens[1])))

    data.append(availableBW[:120])
    data.append(availableBuffer[:120])
    data.append(availableLatency[:120])

def getBitrates(jsonFile):
    dataRates = []
    with(open(jsonFile) as jsonData):
        data = json.load(jsonData)
    for i in data:
        for j in range(0, i["duration"]):
            dataRates.append(int(i["clientIngress"]))
    return dataRates[:120]

def getVideoBitrates(mpd, log):
    targets = []
    bw = []
    bwSet = []
    with(open(log) as log):
        targets = [line for line in log if "chunk-stream" in line]
        targets = [line.split("_",1)[1].split("-",1)[0] for line in targets]
        targets = list(int(i) for i in targets)
        targets[:] = (value for value in targets if value != 7)

    mpd = ET.parse(mpd)
    root = mpd.getroot()
    for idx,log_element in enumerate(root.findall('.//{urn:mpeg:dash:schema:mpd:2011}Representation')):
        bw.append(log_element.attrib['bandwidth'])

    for i in targets:
        bwSet.append(int(bw[i]))
    return bwSet

def calcQoE():
    bwSet = getVideoBitrates(sys.argv[4], sys.argv[5])
    numChunks = len(bwSet)
    w1 = 0.8469
    w2 = 28.7959
    w3 = 0.2979
    w4 = 1.0610
    qoe = 0
    n1 = sum(bwSet)
    n2 = 0
    n3 = 0
    n4 = 0

    for i in range(0, len(stalls)):
            n2 += float(stalls[i][2])

    for i in range(0, numChunks-1):
        _val = bwSet[i+1] - bwSet[i]
        if(_val > 0):
            n3 += abs(_val)
        else:
            n4 += abs(_val)
    
    qoe = w1*n1 - w2*n2 + w3*n3 - w4*n4
    return (qoe)
    

if __name__ == "__main__":
    getData(sys.argv[1])
    getData(sys.argv[2])
    qoeArray = []
    with open("QoE.txt", "a") as f:
        f.write(str(calcQoE()))
        f.write("\n")

    figure, axis = plt.subplots(3)
    figure.legend()
    axis[0].plot(getBitrates(sys.argv[3]), color="green", label="givenBW")
    axis[0].plot(data[0], color="red", label="proxy")
    axis[0].plot(data[3], color="blue", label="ws")
    axis[0].set_title("availableBW")
    axis[1].plot(data[1], color="red", label="proxy")
    axis[1].plot(data[4], color="blue", label="ws")
    axis[1].set_title("availableBuffer")
    axis[2].plot(data[2], color="red", label="proxy")
    axis[2].plot(data[5], color="blue", label="ws")
    axis[2].set_title("availableLatency")
    plt.tight_layout()
    plt.savefig(f'{sys.argv[2]}_figure.png')

    plt.show()