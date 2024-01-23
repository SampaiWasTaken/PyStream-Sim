import matplotlib.pyplot as plt
# import pandas as pd
import re

# class Client:
#     def __init__(self, name, cpu, mem):
#         self.name = name
#         self.cpu = cpu
#         self.mem = mem

#     def __getAvgCPU__(self):
#         return (sum(self.cpu)) / len(self.cpu)
    
#     def __getAvgMem__(self):
#         return (sum(self.mem)) / len(self.mem)

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
    cpu = []
    mem = []
    ns_CPU = []
    ns_MEM = []
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
                            cpu_percent = clean_string(parts[1]).replace('%', '')
                            if cpu_percent != '0.0':
                                if parts[0].__contains__('ns'):
                                    ns_CPU.append(float(cpu_percent))
                                else:
                                    cpu.append(float(cpu_percent))  
                            mem_usage = parse_memory(clean_string(parts[2]))
                            if mem_usage != 0.0:
                                if parts[0].__contains__('ns'):
                                    ns_MEM.append(mem_usage)
                                else:
                                    mem.append(mem_usage)
    # return sum(cpu)/len(cpu), sum(mem)/len(mem), sum(ns_CPU)/len(ns_CPU), sum(ns_MEM)/len(ns_MEM)
    return cpu, mem, ns_CPU, ns_MEM

# Plotting
cpu5, mem5, ns_cpu5, ns_mem5 = getData(5)
cpu10, mem10, ns_cpu10, ns_mem10 = getData(10)
cpu25, mem25, ns_cpu25, ns_mem25 = getData(25)
cpu50, mem50, ns_cpu50, ns_mem50 = getData(50)


fig = plt.figure(figsize=(30, 5))
ax1 = plt.subplot2grid((6, 100), (0, 0), colspan=20, rowspan=5)
ax1.set_ylabel('',fontsize=13)
ax1.set_ylabel('CPU Usage of Clients [%]',fontsize=13)
ax1.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax1.set_title('Ramp Up',fontsize=15)

ax2 = plt.subplot2grid((6, 100), (0, 25), colspan=20, rowspan=5)
ax2.set_ylabel('RAM Usage of Clients [MiB]',fontsize=13)
ax2.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax2.set_title('Ramp Down',fontsize=15)

ax3 = plt.subplot2grid((6, 100), (0, 50), colspan=20, rowspan=5)
ax3.set_ylabel('CPU Usage of Controller [%]',fontsize=13)
ax3.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax3.set_title('Cascade',fontsize=15)

ax4 = plt.subplot2grid((6, 100), (0, 75), colspan=20, rowspan=5)
ax4.set_ylabel('RAM Usage of Controller [MiB]',fontsize=13)
ax4.set_xlabel('Number of Concurrent Clients',fontsize=13)
# ax4.set_title('Steps',fontsize=15)

bplot1 = ax1.boxplot([cpu5, cpu10, cpu25, cpu50], labels=[5, 10, 25, 50])
bplot2 = ax2.boxplot([mem5, mem10, mem25, mem50], labels=[5, 10, 25, 50])
bplot3 = ax3.boxplot([ns_cpu5, ns_cpu10,ns_cpu25, ns_cpu50], labels=[5, 10, 25, 50])
bplot4 = ax4.boxplot([ns_mem5, ns_mem10,ns_mem25, ns_mem50], labels=[5, 10, 25, 50])

# ax1.set_xticks([1.5,4.5,7.5,10.5],['5','10','25', '50'])
plt.savefig('ResourceClient.png')
plt.show()