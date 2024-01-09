import matplotlib.pyplot as plt
from random import randint
import json, re

data = list()

def lines_that_contain(string, fp):
    return [line for line in fp if string in line]

#Find the stall data in the log file and process it, splitting into bandwidth, buffer and latency
#@param numIt: number of iterations i.e. number of log files
#@param file: log file name
def getData(numIt, file):
    global stalls
    data = [0] * 120
    if numIt == 1:
        stalls = lines_that_contain("stall", open(file+"1.log", "r"))[0].split("\"",1)[1].split("source",1)[0][:-3]
        stalls = stalls.replace("null", "0")
        stalls = stalls.replace("\"", "")
        tokens = stalls.split("availibleBW")
        stalls = re.findall(r'\[(\d*\.*\d*),(\d*\.*\d*),(\d*\.*\d*)\]', tokens[0])
        tokens = tokens[1].split("currentBuffer")
        availableBW = list(map(float,re.findall(r'\d+',tokens[0])))
        tokens = tokens[1].split("currentLatency")
        availableBuffer = list(map(float, re.findall(r'\d+\.*\d*',tokens[0])))
        availableLatency = list(map(float, re.findall(r'\d+\.*\d*',tokens[1])))

        #only bandwidth is used here
        data = availableBW
        # print(data)
        return data[:119]
    #In case it is only a single file (not iterable)
    for i in range(1, numIt+1):
        # print(i)
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

        data = [a+b for a,b in zip(data, availableBW)]
        # print(data)

    data[:] = [x / numIt for x in data]
    # print(data)
    return data[:118]

#Function to get the bitrates from the nettrace json file
def getBitrates(jsonFile):
    dataRates = []
    with(open(jsonFile) as jsonData):
        data = json.load(jsonData)
    for i in data:
        for j in range(0, i["duration"]):
            dataRates.append(int(i["clientIngress"]))
    return dataRates[:119]

#Function to get the mean absolute error
def getMeanError(bw, br):
    error = [abs(a-b) for a,b in zip(bw, br)]
    return sum(error)/len(error)

#Function to get the variance
def getVariance(bw, br):
    variance = []
    for i in range(len(br)):
        diff = abs(bw[i] - br[i])
        variance.append(diff)
    return variance[:118]

#######################################################################################################################

#Fetch the data from the log files here
#Data vetting might be needed in case some stall files are created a few seconds early, leading to shorter data

# update for Nettrance 1
net_trace1=getBitrates('netTraces/BelgiumBus.json')[:118]
pystream1=getData(20, "logs/belgiumBus/load_25_belgiumBus")[:118]
wonder1=getData(20, "logs/belgiumBus/Cadvise/cadvise_belgiumBus")[:118]

#update for Nettrance 2
net_trace2=getBitrates('netTraces/BelgiumBicycle.json')[:118]
pystream2=getData(20, "logs/belgiumBicycle/load_25_belgiumBicycle")[:118]
wonder2=getData(20, "logs/belgiumBicycle/Cadvise/cadvise_belgiumBicycle")[:118]

#update for Nettrance 3
net_trace3=getBitrates('netTraces/cascade.json')[:118]
pystream3=getData(20, "logs/Cascade/cascade")[:118]
wonder3=getData(20, "logs/cascade/cadvise/cadvise_cascade")[:118]

#update for Nettrance 4
net_trace4=getBitrates('netTraces/steps.json')[:118]
pystream4=getData(20, "logs/Steps/steps")[:118]
wonder4=getData(20, "logs/Steps/Cadvise/cadvise_steps")[:118]

# net_trace1=getBitrates('netTraces/stable.json')[:118]
# pystream1=getData(20, "logs/stable/load_25_stable")[:118]
# wonder1=getData(20, "logs/stable/Cadvise/cadvise_stable")[:118]

# #update for Nettrance 2
# net_trace2=getBitrates('netTraces/rampUp.json')[:118]
# pystream2=getData(20, "logs/rampUp/load_25_rampUp")[:118]
# wonder2=getData(20, "logs/rampUp/Cadvise/cadvise_rampUp")[:118]

# #update for Nettrance 3
# net_trace3=getBitrates('netTraces/rampDown.json')[:118]
# pystream3=getData(20, "logs/rampDown/load_25_rampDown")[:118]
# wonder3=getData(20, "logs/rampDown/Cadvise/cadvise_rampDown")[:118]

#######################################################################################################################

#update for Nettrance 1
me_pystream_original1=getMeanError(net_trace1, pystream1) #player 2
me_wonder_original1=getMeanError(net_trace1, wonder1)
var_pystream_original1=getVariance(net_trace1, pystream1)
var_wonder_original1=getVariance(net_trace1, wonder1)
#update for Nettrance 2
me_pystream_original2=getMeanError(net_trace2, pystream2) #player 2
me_wonder_original2=getMeanError(net_trace2, wonder2)
var_pystream_original2=getVariance(net_trace2, pystream2)
var_wonder_original2=getVariance(net_trace2, wonder2)
#update for Nettrance 3
me_pystream_original3=getMeanError(net_trace3, pystream3) #player 2
me_wonder_original3=getMeanError(net_trace3, wonder3)
var_pystream_original3=getVariance(net_trace3, pystream3)
var_wonder_original3=getVariance(net_trace3, wonder3)

#update for Nettrance 4
me_pystream_original4=getMeanError(net_trace4, pystream4) #player 2
me_wonder_original4=getMeanError(net_trace4, wonder4)
var_pystream_original4=getVariance(net_trace4, pystream4)
var_wonder_original4=getVariance(net_trace4, wonder4)

#######################################################################################################################

fig = plt.figure(figsize=(30, 5))
ax1 = plt.subplot2grid((6, 100), (0, 0), colspan=100, rowspan=6)
ax1.set_ylabel('',fontsize=13)
ax1.set_xlabel('MAE of Different Network Traces',fontsize=13)

ax1.bar([1,2],[me_pystream_original1, me_wonder_original1],color=['tab:blue','tab:red'],label=['Diff. PyStreamShaper and Original','Diff. CAdViSE and Original'])
# Error bar has a dimension error here, not sure why.
# ax1.errorbar([1,2],[me_pystream_original1, me_wonder_original1],yerr=[var_pystream_original1, var_wonder_original1],fmt="o",color='black')

ax1.bar([4,5],[me_pystream_original2, me_wonder_original2],color=['tab:blue','tab:red'])
# ax1.errorbar([4,5],[me_pystream_original2, me_wonder_original2],yerr=[var_pystream_original2, var_wonder_original2],fmt="o",color='black')

ax1.bar([7,8],[me_pystream_original3, me_wonder_original3],color=['tab:blue','tab:red'])
# ax1.errorbar([7,8],[me_pystream_original3, me_wonder_original3],yerr=[var_pystream_original3, var_wonder_original3],fmt="o",color='black')

ax1.bar([10,11],[me_pystream_original4, me_wonder_original4],color=['tab:blue','tab:red'])
# ax1.errorbar([10,11],[me_pystream_original4, me_wonder_original4],yerr=[var_pystream_original4, var_wonder_original4],fmt="o",color='black')

ax1.legend(fontsize=13)
ax1.set_xticks([1.5,4.5,7.5,10.5],['belgiumBicycle','belgiumBus','Cascade', 'Steps'])
plt.savefig('Figures/diff_bus_bicycle_steps_cascade.png')
# plt.savefig('diff_stable_ramps.png')

plt.show()