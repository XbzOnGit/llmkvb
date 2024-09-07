import sys
from matplotlib import pyplot as plt
assert len(sys.argv) == 5
class ExpItem:
    def __init__(self, qps, thput, avg_ttft):
        self.qps = qps
        self.thput = thput
        self.avg_ttft = avg_ttft


plot_dir = sys.argv[1]
qps_str = sys.argv[2]
thput_str = sys.argv[3]
avg_ttft_str = sys.argv[4]
qps = [float(x) for x in qps_str.split(',')]
thput = [float(x) for x in thput_str.split(',')]
avg_ttft = [float(x) for x in avg_ttft_str.split(',')]
assert len(qps) == len(thput) and len(thput) == len(avg_ttft)
exp_items = []
for i in range(len(qps)):
    exp_items.append(ExpItem(qps[i], thput[i], avg_ttft[i]))
exp_items.sort(key=lambda x: x.qps)
qps = [x.qps for x in exp_items]
thput = [x.thput for x in exp_items]
avg_ttft = [x.avg_ttft for x in exp_items]
# y-axis should start from 0.
plt.plot(qps, thput)
plt.xlabel('QPS')
plt.ylabel('Throughput(req/s)')
plt.title('QPS vs Throughput')
plt.ylim(bottom=0)
plt.savefig(f"{plot_dir}/qps_vs_throughput.png")
plt.clf()
plt.plot(qps, avg_ttft)
plt.xlabel('QPS')
plt.ylabel('Avg TTFT(s)')
plt.title('QPS vs Avg TTFT')
plt.ylim(bottom=0)
plt.savefig(f"{plot_dir}/qps_vs_avg_ttft.png")