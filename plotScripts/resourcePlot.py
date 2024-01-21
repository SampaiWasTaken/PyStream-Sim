import matplotlib.pyplot as plt
import pandas as pd
import re

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

def main():
    data = {
        'NAME': [],
        'CPU %': [],
        'MEM USAGE(MiB)': []
    }

    with open('mystats.txt', 'r', encoding="utf-16") as file:
        next(file)  # Skip header line
        for line in file:
            if line.strip():  # Skip empty lines``
                if line.__contains__('NAME'):
                    continue
                else:
                    parts = re.split(r" {2,}", line)
                    if len(parts) == 3:
                        data['NAME'].append(clean_string(parts[0]))
                        cpu_percent = clean_string(parts[1]).replace('%', '')
                        data['CPU %'].append(float(cpu_percent))
                        mem_usage = parse_memory(clean_string(parts[2]))
                        data['MEM USAGE(MiB)'].append(mem_usage)

    df = pd.DataFrame(data)
    print(df['NAME'])
    
    # Plotting
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('NAME')
    ax1.set_ylabel('CPU %', color=color)
    ax1.bar(df['NAME'], df['CPU %'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('MEM USAGE(MiB)', color=color)
    ax2.bar(df['NAME'], df['MEM USAGE(MiB)'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
