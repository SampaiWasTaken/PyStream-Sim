import matplotlib.pyplot as plt
from random import random
import json, re


data = list()

#Function to get data from log file
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
    return data

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
    for i in range(len(bw)):
        diff = abs(bw[i] - br[i])
        variance.append(diff)
    return variance

#######################################################################################################################

#Get the data from the log files here
#Data vetting might be needed in case some stall files are created a few seconds early, leading to shorter data


# update for Nettrance 1
net_trace1=getBitrates('netTraces/rampUp.json')[:118]
pystream1=getData(20, "logs/rampUp/load_25_rampUp")[:118]
wonder1=getData(20, "logs/rampUp/Cadvise/cadvise_rampUp")[:118]
tp1=getData(20, "logs/rampUp/Throughput/rampUp_throughput")[:118]
tpw1=getData(20, "logs/rampUp/Throughput/cadvise_rampUp_throughput")[:118]

#update for Nettrance 2
net_trace2=getBitrates('netTraces/rampDown.json')[:118]
pystream2=getData(20, "logs/rampDown/load_25_rampDown")[:118]
wonder2=getData(20, "logs/rampDown/Cadvise/cadvise_rampDown")[:118]
tp2=getData(20, "logs/rampDown/Throughput/rampDown_throughput")[:118]
tpw2=getData(20, "logs/rampDown/Throughput/cadvise_rampDown_throughput")[:118]

#update for Nettrance 3
net_trace3=getBitrates('netTraces/cascade.json')[:118]
pystream3=getData(20, "logs/Cascade/load_25_cascade")[:118]
wonder3=getData(20, "logs/cascade/Cadvise/cadvise_cascade")[:118]
tp3=getData(20, "logs/Cascade/Throughput/cascade_throughput")[:118]
tpw3=getData(20, "logs/cascade/Throughput/cadvise_cascade_throughput")[:118]

#update for Nettrance 4
net_trace4=getBitrates('netTraces/steps.json')[:118]
pystream4=getData(20, "logs/Steps/load_25_steps")[:118]
wonder4=getData(20, "logs/Steps/Cadvise/cadvise_steps")[:118]
tp4=getData(20, "logs/Steps/Throughput/steps_throughput")[:118]
tpw4=getData(20, "logs/Steps/Throughput/cadvise_steps_throughput")[:118]

#update for Nettrance 5
net_trace5=getBitrates('netTraces/stable.json')[:118]
pystream5=getData(20, "logs/stable/load_25_stable")[:118]
wonder5=getData(20, "logs/stable/Cadvise/cadvise_stable")[:118]
tp5=getData(20, "logs/stable/Throughput/stable_throughput")[:118]
tpw5=getData(20, "logs/stable/Cadvise/cadvise_stable")[:118] #Throughput ABR for stable for Cadvise missing


# #update for Nettrance 5
# net_trace4=getBitrates('netTraces/steps.json')[:118]
# pystream4=getData(20, "logs/Steps/Throughput/steps_throughput")[:118]
# wonder4=getData(20, "logs/Steps/Throughput/cadvise_steps_throughput")[:118]

# #update for Nettrance 2
# net_trace2=getBitrates('netTraces/rampUp.json')[:118]
# pystream2=getData(20, "logs/rampUp/load_25_rampUp")[:118]
# wonder2=getData(20, "logs/rampUp/Cadvise/cadvise_rampUp")[:118]

# #update for Nettrance 3
# net_trace3=getBitrates('netTraces/rampDown.json')[:118]
# pystream3=getData(20, "logs/rampDown/load_25_rampDown")[:118]
# wonder3=getData(20, "logs/rampDown/Cadvise/cadvise_rampDown")[:118]

#######################################################################################################################

#Plot the data here

fig = plt.figure(figsize=(30, 5))
ax1 = plt.subplot2grid((6, 125), (0, 0), colspan=20, rowspan=5)
ax1.set_xlabel('streaming time (s)',fontsize=13)
ax1.set_ylabel('Bitrate (bps)',fontsize=13)
ax1.set_title('Net. Trace: Ramp Up',fontsize=13)
ax1.set_ylim([0,10000])

ax2 = plt.subplot2grid((6, 125), (0, 25), colspan=20, rowspan=5)
ax2.set_xlabel('streaming time (s)',fontsize=13)
ax2.set_ylabel('Bitrate (bps)',fontsize=13)
ax2.set_title('Net. Trace: Ramp Down',fontsize=13)
ax2.set_ylim([0,10000])

ax3 = plt.subplot2grid((6, 125), (0, 50), colspan=20, rowspan=5)
ax3.set_xlabel('streaming time (s)',fontsize=13)
ax3.set_ylabel('Bitrate (bps)',fontsize=13)
ax3.set_title('Net. Trace: Cascade',fontsize=13)
ax3.set_ylim([0,10000])

ax4 = plt.subplot2grid((6, 125), (0, 75), colspan=20, rowspan=5)
ax4.set_xlabel('streaming time (s)',fontsize=13)
ax4.set_ylabel('Bitrate (bps)',fontsize=13)
ax4.set_title('Net. Trace: Steps',fontsize=13)
ax4.set_ylim([0,10000])

ax5 = plt.subplot2grid((6, 125), (0, 100), colspan=20, rowspan=5)
ax5.set_xlabel('streaming time (s)',fontsize=13)
ax5.set_ylabel('Bitrate (bps)',fontsize=13)
ax5.set_title('Net. Trace: Stable',fontsize=13)
ax5.set_ylim([0,10000])

# fig = plt.figure(figsize=(30, 5))
# ax1 = plt.subplot2grid((6, 100), (0, 0), colspan=20, rowspan=5)
# ax1.set_xlabel('streaming time (s)',fontsize=13)
# ax1.set_ylabel('Bitrate (bps)',fontsize=13)
# ax1.set_title('Net. Trace: Stable',fontsize=13)
# ax1.set_ylim([0,10000])

# ax2 = plt.subplot2grid((6, 100), (0, 25), colspan=20, rowspan=5)
# ax2.set_xlabel('streaming time (s)',fontsize=13)
# ax2.set_ylabel('Bitrate (bps)',fontsize=13)
# ax2.set_title('Net. Trace: RampUp',fontsize=13)
# ax2.set_ylim([0,10000])

# ax3 = plt.subplot2grid((6, 100), (0, 50), colspan=20, rowspan=5)
# ax3.set_xlabel('streaming time (s)',fontsize=13)
# ax3.set_ylabel('Bitrate (bps)',fontsize=13)
# ax3.set_title('Net. Trace: RampDown',fontsize=13)
# ax3.set_ylim([0,10000])


ax1.plot([i for i in range(len(net_trace1))],net_trace1,label='Original Net. Trace',color='tab:green')
ax1.plot([i for i in range(len(pystream1))],pystream1,label='PyStreamShaper - L2A',color='tab:blue')
ax1.plot([i for i in range(len(wonder1))],wonder1,label='CAdViSE - L2A',color='tab:red')
ax1.plot([i for i in range(len(tp1))],tp1,label='PyStreamShaper - Throughput',color='tab:blue', linestyle='dashed')
ax1.plot([i for i in range(len(tpw1))],tpw1,label='CAdViSE - Throughput',color='tab:red', linestyle='dashed')

ax2.plot([i for i in range(len(net_trace2))],net_trace2,label='Original Net. Trace',color='tab:green')
ax2.plot([i for i in range(len(pystream2))],pystream2,label='PyStreamShaper',color='tab:blue')
ax2.plot([i for i in range(len(wonder2))],wonder2,label='CAdViSE',color='tab:red')
ax2.plot([i for i in range(len(tp2))],tp2,label='PyStreamShaper - Throughput',color='tab:blue', linestyle='dashed')
ax2.plot([i for i in range(len(tpw2))],tpw2,label='CAdViSE - Throughput',color='tab:red', linestyle='dashed')

ax3.plot([i for i in range(len(net_trace3))],net_trace3,label='Original Net. Trace',color='tab:green')
ax3.plot([i for i in range(len(pystream3))],pystream3,label='PyStreamShaper',color='tab:blue')
ax3.plot([i for i in range(len(wonder3))],wonder3,label='CAdViSE',color='tab:red')
ax3.plot([i for i in range(len(tp3))],tp3,label='PyStreamShaper - Throughput',color='tab:blue', linestyle='dashed')
ax3.plot([i for i in range(len(tpw3))],tpw3,label='CAdViSE - Throughput',color='tab:red', linestyle='dashed')

ax4.plot([i for i in range(len(net_trace4))],net_trace4,label='Original Net. Trace',color='tab:green')
ax4.plot([i for i in range(len(pystream4))],pystream4,label='PyStreamShaper',color='tab:blue')
ax4.plot([i for i in range(len(wonder4))],wonder4,label='CAdViSE',color='tab:red')
ax4.plot([i for i in range(len(tp4))],tp4,label='PyStreamShaper - Throughput',color='tab:blue', linestyle='dashed')
ax4.plot([i for i in range(len(tpw4))],tpw4,label='CAdViSE - Throughput',color='tab:red', linestyle='dashed')

ax5.plot([i for i in range(len(net_trace5))],net_trace5,label='Original Net. Trace',color='tab:green')
ax5.plot([i for i in range(len(pystream5))],pystream5,label='PyStreamShaper',color='tab:blue')
ax5.plot([i for i in range(len(wonder5))],wonder5,label='CAdViSE',color='tab:red')
ax5.plot([i for i in range(len(tp5))],tp5,label='PyStreamShaper - Throughput',color='tab:blue', linestyle='dashed')
ax5.plot([i for i in range(len(tpw5))],tpw5,label='CAdViSE - Throughput',color='tab:red', linestyle='dashed')


# ax1.legend(fontsize=13)
# ax2.legend(fontsize=13)
# ax3.legend(fontsize=13)
# ax4.legend(fontsize=13)
# ax5.legend(fontsize=13)

handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles, labels, loc="outside center", bbox_to_anchor=(0.5,-0.2), ncol=5, fontsize=13)
plt.legend(handles, labels, bbox_to_anchor=(0,-0.2), ncol=5, fontsize=13)
# plt.savefig('nettraces_bus_bicycle_steps_cascade.png')
plt.tight_layout()
plt.savefig('Figures/ABR_Traces.png')

plt.show()