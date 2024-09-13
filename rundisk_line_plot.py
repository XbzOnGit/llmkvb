import sys
from matplotlib import pyplot as plt
if __name__ == '__main__':
    assert len(sys.argv) == 2, 'Usage: python rundisk_line_plot.py <param_list>'
    param_list = sys.argv[1]
    print(f"param_list: {param_list}")
    paper_name_end = param_list.find(';')
    paper_names = param_list[:paper_name_end].split('~')
    param_list = param_list[paper_name_end+1:]
    results_list = param_list.split(';')
    general_qps_list = []
    general_throughput_list = []
    general_avg_ttft_list = []
    for i in range(len(paper_names)):
        paper_name = paper_names[i]
        result_pack = results_list[i].split('-')
        qps_list = result_pack[0].split(',')
        throughput_list = result_pack[1].split(',')
        avg_ttft_list = result_pack[2].split(',')
        print(f"paper_name: {paper_name}")
        print(f"qps_list: {qps_list}")
        print(f"throughput_list: {throughput_list}")
        print(f"avg_ttft_list: {avg_ttft_list}")
        qps_list = [float(qps) for qps in qps_list] # x-axis
        throughput_list = [float(throughput) for throughput in throughput_list] # y-axis for graph 1.
        avg_ttft_list = [float(avg_ttft) for avg_ttft in avg_ttft_list] # y-axis for graph 2.
        general_qps_list.append(qps_list)
        general_throughput_list.append(throughput_list)
        general_avg_ttft_list.append(avg_ttft_list)
    
    for i in range(len(paper_names)):
        plt.plot(general_qps_list[i], general_throughput_list[i], label=paper_names[i])
    plt.title("QPS-Throughput")
    plt.xlabel("QPS")
    plt.ylabel("Throughput req/s")
    plt.legend()
    plt.savefig("qps_throughput.png")
    plt.clf()
    for i in range(len(paper_names)):
        plt.plot(general_qps_list[i], general_avg_ttft_list[i], label=paper_names[i])
    plt.title("QPS-AvgTTFT")
    plt.xlabel("QPS")
    plt.ylabel("AvgTTFT second")
    plt.legend()
    plt.savefig("qps_avg_ttft.png")
    plt.clf()

