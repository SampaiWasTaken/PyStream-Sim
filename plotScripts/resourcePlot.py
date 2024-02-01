import matplotlib.pyplot as plt
import numpy as np
from operator import add
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
                            if parts[0] == "ns":
                                cpu_percent = clean_string(parts[1]).replace('%', '')
                                if float(cpu_percent) > 20:
                                    clientDic[parts[0]].cpu.append(float(cpu_percent))

                                mem_usage = parse_memory(clean_string(parts[2]))
                                if float(mem_usage) > 0.2:
                                    clientDic[parts[0]].mem.append(mem_usage)
                            else:
                                cpu_percent = clean_string(parts[1]).replace('%', '')
                                if float(cpu_percent) > 0.2:
                                    clientDic[parts[0]].cpu.append(float(cpu_percent))

                                mem_usage = parse_memory(clean_string(parts[2]))
                                if float(mem_usage) > 0.2:
                                    clientDic[parts[0]].mem.append(mem_usage)
    # return sum(cpu)/len(cpu), sum(mem)/len(mem), sum(ns_CPU)/len(ns_CPU), sum(ns_MEM)/len(ns_MEM)
    return clientDic

def getValues(clientDic):
    ns_cpu = 0
    ns_mem = 0
   
    client_cpu = 0
    client_mem = 0

    var_mem = 0
    var_cpu = 0
    
    
    threadPercent = 12800
    maxRam = 252416
    with open ("Variance.txt", "a") as f:
        f.write(f'--------------------------Scenario: {len(clientDic)} Clients--------------------------\n')
        for key in clientDic:
            f.write(f'Standard Deviation of {key}: CPU = {str(np.std(clientDic[key].cpu))} | MEM = {str(np.std(clientDic[key].mem))}\n')
            if key == "ns":
                ns_cpu = np.mean(clientDic[key].cpu)
                ns_mem += np.mean(clientDic[key].mem)
                var_cpu += np.var(clientDic[key].cpu)
                var_mem += np.var(clientDic[key].mem)
            else:
                client_cpu += np.mean(clientDic[key].cpu)
                client_mem += np.mean(clientDic[key].mem)
                var_cpu += np.var(clientDic[key].cpu)
                var_mem += np.var(clientDic[key].mem)
    return client_cpu/threadPercent, client_mem/maxRam, ns_cpu/threadPercent, ns_mem/maxRam, np.sqrt(var_cpu)/threadPercent, np.sqrt(var_mem)/maxRam

# # Plotting
# cpu5 , mem5, ns_cpu5, ns_mem5 = getValues(getData(5))
# cpu10, mem10, ns_cpu10, ns_mem10 = getValues(getData(10))
# cpu25, mem25, ns_cpu25, ns_mem25 = getValues(getData(25))
# cpu50, mem50, ns_cpu50, ns_mem50 = getValues(getData(50))


cpu8,   mem8,   ns_cpu8,    ns_mem8,    var_cpu8,    var_mem8     = getValues(getData(8))
cpu16,  mem16,  ns_cpu16,   ns_mem16,   var_cpu16,   var_mem16    = getValues(getData(16))
cpu32,  mem32,  ns_cpu32,   ns_mem32,   var_cpu32,   var_mem32    = getValues(getData(32))
cpu64,  mem64,  ns_cpu64,   ns_mem64,   var_cpu64,   var_mem64    = getValues(getData(64))
cpu128, mem128, ns_cpu128,  ns_mem128,  var_cpu128,  var_mem128   = getValues(getData(128))
# cpu256, mem256, ns_cpu256, ns_mem256 = getValues(getData(256))

fig = plt.figure(figsize=(30, 5))
ax1 = plt.subplot2grid((6, 50), (0, 0), colspan=20, rowspan=5)
ax1.set_ylabel('',fontsize=13)
ax1.set_ylabel('CPU Usage [%]',fontsize=13)
ax1.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax1.set_title('Ramp Up',fontsize=15)

ax2 = plt.subplot2grid((6, 50), (0, 25), colspan=20, rowspan=5)
ax2.set_ylabel('RAM Usage [%]',fontsize=13)
ax2.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax2.set_title('Ramp Down',fontsize=15)

ax1.set_ylim(0, 1)
ax2.set_ylim(0, 0.2)

labels = ['8', '16', '32', '64', '128']
ns_cpu_data = [ns_cpu8, ns_cpu16,ns_cpu32, ns_cpu64, ns_cpu128]
ns_mem_data = [ns_mem8, ns_mem16,ns_mem32, ns_mem64, ns_mem128]
cpu_data = [cpu8, cpu16, cpu32, cpu64, cpu128]
mem_data = [mem8, mem16, mem32, mem64, mem128]

cpu_data_sum = [x + y for x, y in zip(cpu_data, ns_cpu_data)]
mem_data_sum = [x + y for x, y in zip(mem_data, ns_mem_data)]

cpu_vars = [var_cpu8, var_cpu16, var_cpu32, var_cpu64, var_cpu128]
mem_vars = [var_mem8, var_mem16, var_mem32, var_mem64, var_mem128]

print(cpu_vars)

bplot1 = ax1.bar(labels, cpu_data, color='blue', label='Clients')
bplot2 = ax1.bar(labels, ns_cpu_data, color='red', label='Controller', bottom=cpu_data)

bplot3 = ax2.bar(labels, mem_data, color='blue', label='Clients')
bplot4 = ax2.bar(labels, ns_mem_data, color='red', label='Controller', bottom=mem_data)

ax1.errorbar(labels, cpu_data_sum, yerr=cpu_vars, ecolor='black', capsize=3, ls='none')
ax2.errorbar(labels, mem_data_sum, yerr=mem_vars, ecolor='black', capsize=3, ls='none')


# ax1.set_xticks([1.5,4.5,7.5,10.5],['5','10','25', '50'])
plt.legend
# plt.legend([bplot1, bplot2, bplot3, bplot4], ['Clients CPU', 'Clients RAM', 'Controller CPU', 'Controller RAM'], loc='upper left', fontsize=13)
ax1.legend([bplot1, bplot2], ['Clients', 'Controller'])
ax2.legend([bplot3, bplot4], ['Clients', 'Controller'])

plt.savefig('Figures/ResourcePlot_new.png')

plt.show()