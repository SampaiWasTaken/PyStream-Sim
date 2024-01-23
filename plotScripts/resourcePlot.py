import matplotlib.pyplot as plt
import numpy as np
# import pandas as pd
import re

class Client:
    def __init__(self, name, cpu, mem):
        self.name = name
        self.cpu = cpu
        self.mem = mem

    def __getAvgCPU__(self):
        return (sum(self.cpu)) / len(self.cpu)
    
    def __getAvgMem__(self):
        return (sum(self.mem)) / len(self.mem)

def parse_memory(mem_str):
    mem, _ = mem_str.split('/')
    if 'GiB' in mem:
        return float(mem.replace('GiB', '').strip()) * 1024
    elif 'MiB' in mem:
        return float(mem.replace('MiB', '').strip())
    else:
        return 0.0

def clean_string(s):
    return ''.join(char for char in s if char.isprintable())

def getData(numClients):
    clientDic = {}
    with open(f'PerformanceLogs_{numClients}.txt', 'r') as file:
        next(file)  # Skip header line
        for line in file:
            if line.strip():  # Skip empty lines``
                if line.__contains__('NAME'):
                    continue
                else:
                    parts = re.split(r" {2,}", line)
                    if len(parts) == 3:
                        for i in range(len(parts)):
                            if parts[i] == "--":
                                parts[i] = "0.0"
                        # data['NAME'].append(clean_string(parts[0]))
                        if not parts[0].__contains__('0.0'):
                            if parts[0] not in clientDic:
                                clientDic[parts[0]] = Client(parts[0], [], [])

                            cpu_percent = clean_string(parts[1]).replace('%', '')
                            if cpu_percent != '0.0':
                                clientDic[parts[0]].cpu.append(float(cpu_percent))

                            mem_usage = parse_memory(clean_string(parts[2]))
                            if mem_usage != 0.0:
                                clientDic[parts[0]].mem.append(mem_usage)
    # return sum(cpu)/len(cpu), sum(mem)/len(mem), sum(ns_CPU)/len(ns_CPU), sum(ns_MEM)/len(ns_MEM)
    return clientDic

def getValues(clientDic):
    ns_cpu = 0
    ns_mem = 0
    client_cpu = 0
    client_mem = 0
    print(f'--------------------------Scenario: {len(clientDic)} Clients--------------------------')
    for key in clientDic:
        print(f'Standard Deviation of {key}: CPU = {str(np.std(clientDic[key].cpu))} | MEM = {str(np.std(clientDic[key].mem))}')
        if key == "ns":
            ns_cpu = sum(clientDic[key].cpu)/len(clientDic[key].cpu)
            ns_mem = sum(clientDic[key].mem)/len(clientDic[key].mem)
        else:
            client_cpu += (sum(clientDic[key].cpu)/len(clientDic[key].cpu))
            client_mem += (sum(clientDic[key].mem)/len(clientDic[key].mem))
    return client_cpu/2400, client_mem/15953.92, ns_cpu/2400, ns_mem/15953.92

# Plotting
cpu5 , mem5, ns_cpu5, ns_mem5 = getValues(getData(5))
cpu10, mem10, ns_cpu10, ns_mem10 = getValues(getData(10))
cpu25, mem25, ns_cpu25, ns_mem25 = getValues(getData(25))
cpu50, mem50, ns_cpu50, ns_mem50 = getValues(getData(50))

fig = plt.figure(figsize=(30, 5))
ax1 = plt.subplot2grid((6, 50), (0, 0), colspan=20, rowspan=5)
ax1.set_ylabel('',fontsize=13)
ax1.set_ylabel('CPU Usage of Clients [%]',fontsize=13)
ax1.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax1.set_title('Ramp Up',fontsize=15)

ax2 = plt.subplot2grid((6, 50), (0, 25), colspan=20, rowspan=5)
ax2.set_ylabel('RAM Usage of Clients [%]',fontsize=13)
ax2.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax2.set_title('Ramp Down',fontsize=15)

ax1.set_ylim(0, 1)
ax2.set_ylim(0, 1)

labels = ['5', '10', '25', '50']

bplot3 = ax1.bar(labels, [ns_cpu5, ns_cpu10,ns_cpu25, ns_cpu50], color='red', label='Controller')
bplot1 = ax1.bar(labels, [cpu5, cpu10, cpu25, cpu50], color='blue', label='Clients')
bplot2 = ax2.bar(labels, [mem5, mem10, mem25, mem50], color='blue', label='Clients')
bplot4 = ax2.bar(labels, [ns_mem5, ns_mem10,ns_mem25, ns_mem50], color='red', label='Controller')

# ax1.set_xticks([1.5,4.5,7.5,10.5],['5','10','25', '50'])
plt.legend
# plt.legend([bplot1, bplot2, bplot3, bplot4], ['Clients CPU', 'Clients RAM', 'Controller CPU', 'Controller RAM'], loc='upper left', fontsize=13)
ax1.legend([bplot1, bplot3], ['Clients', 'Controller'])
ax2.legend([bplot2, bplot4], ['Clients', 'Controller'])

plt.savefig('Figures/ResourcePlot.png')

plt.show()