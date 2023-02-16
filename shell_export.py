from prometheus_client import start_http_server, Gauge
import subprocess
import time
import yaml



def read_yaml():
    with open('./config/export.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    metric_names,metric_helps,command_dict,metrics = export_client(data['monitoring'])
    return metric_names,metric_helps,command_dict,metrics

def export_client(monitor_dic):
    metric_names = []
    metric_helps = []
    command_dict = {}
    for monitor in monitor_dic:
        metric_names.append(monitor['name'])
        metric_helps.append(monitor['help'])
        command_dict[monitor['name']] = monitor['command']
    metrics = [Gauge(name, help) for name, help in zip(metric_names, metric_helps)]
    return metric_names,metric_helps,command_dict,metrics

def get_metric_values():
    metric_values = {}
    metric_names,metric_helps,command_dict,metrics = read_yaml()
    for name, cmd in command_dict.items():
        output = subprocess.getstatusoutput(cmd)
        if output[0] == 0:
            value = float(output[1])
            metric_values[name] = value
        else:
            sys.exit(6)
            print("命令执行失败：{}".format(output[1]))
    return metric_values,metrics,metric_names

def update_metrics():
    values,metrics,metric_names = get_metric_values()
    for name, value in values.items():
        metric = metrics[metric_names.index(name)]
        metric.set(value)


def main():
    port = 8000
    start_http_server(port)
    while True:
        update_metrics()
        time.sleep(60)

if __name__ == '__main__':
    main()
