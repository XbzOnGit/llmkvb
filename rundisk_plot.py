import sys
from matplotlib import pyplot as plt
def add_comma_to_num(full_str: str):
    # If there are consecutive digits, add a comma between them.
    # e.g., 1000 -> 1,000
    from_right_to_left = ""
    sidx = len(full_str) - 1
    consecutive_digits = 0
    while sidx >= 0:
        from_right_to_left += full_str[sidx]
        if full_str[sidx].isdigit():
            consecutive_digits += 1
            if consecutive_digits == 3:
                from_right_to_left += ','
                consecutive_digits = 0
        sidx -= 1
    return from_right_to_left[::-1]

assert len(sys.argv) == 6
plot_dir = sys.argv[1]
config_name = sys.argv[2]
config_name = add_comma_to_num(config_name)
paper_name_list = sys.argv[3]
throughput_list = sys.argv[4]
avg_ttft_list = sys.argv[5]
paper = paper_name_list.split(',')
throughput = [float(x) for x in throughput_list.split(',')]
avg_ttft = [float(x) for x in avg_ttft_list.split(',')]
assert len(paper) == len(throughput) and len(throughput) == len(avg_ttft)
# y-axis should start from 0.
plt.bar(paper, throughput)
plt.xlabel('methods')
plt.ylabel('Throughput(req/s)')
plt.title(f'{config_name} Throughput')
plt.savefig(f'{plot_dir}/{config_name}_throughput.png')
plt.clf()
plt.bar(paper, avg_ttft)
plt.xlabel('methods')
plt.ylabel('Average TTFT(s)')
plt.title(f'{config_name} Average TTFT')
plt.savefig(f'{plot_dir}/{config_name}_avg_ttft.png')
plt.clf()