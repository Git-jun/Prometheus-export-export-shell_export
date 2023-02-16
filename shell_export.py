from prometheus_client import start_http_server, Gauge
import logging,datetime,os
import subprocess
import time
import yaml

LOG = logging.getLogger(__name__)

def read_yaml():
    LOG.info("Start reading the configuration file ==> ./config/export.yaml ")
    with open('./config/export.yaml', 'r') as f:
        data = yaml.safe_load(f)
    LOG.info("Convert yaml format files to python values ==> {}".format(data)) 
    metric_names,metric_helps,command_dict,metrics = export_client(data['monitoring'])
    port = data['EXPORT-ENV'][0]['port']
    
    return metric_names,metric_helps,command_dict,metrics,port

def export_client(monitor_dic):
    metric_names = []
    metric_helps = []
    command_dict = {}
    for monitor in monitor_dic:
        metric_names.append(monitor['name'])
        metric_helps.append(monitor['help'])
        command_dict[monitor['name']] = monitor['command']
    metrics = [Gauge(name, help) for name, help in zip(metric_names, metric_helps)]
    LOG.info("metric_names: {}\nmetric_helps: {}\ncommand_dict: {}".format(metric_names,metric_helps,command_dict))
    return metric_names,metric_helps,command_dict,metrics

def get_metric_values(metric_names,metric_helps,command_dict,metrics):
    metric_values = {}
    for name, cmd in command_dict.items():
        output = subprocess.getstatusoutput(cmd)
        if output[0] == 0:
            value = float(output[1])
            metric_values[name] = value
        else:
            LOG.info("command execution failed : {}".format(output[1]))
            sys.exit(6)
    return metric_values,metrics,metric_names

def update_metrics(metric_names,metric_helps,command_dict,metrics):
    values,metrics,metric_names = get_metric_values(metric_names,metric_helps,command_dict,metrics)
    LOG.info("Monitor output：{}".format(values))
    for name, value in values.items():
        metric = metrics[metric_names.index(name)]
        metric.set(value)


def main():
    metric_names,metric_helps,command_dict,metrics,port = read_yaml()
    start_http_server(port)
    while True:
        update_metrics(metric_names,metric_helps,command_dict,metrics)
        time.sleep(10)

def _config_logging():
    level = logging.INFO
    #if conf.debug:
    #    level = logging.DEBUG
    filename = os.path.basename(__file__)
    today = datetime.date.today()
    filename = filename + str(today)
    path = '{}.log'.format(filename)

    logging.basicConfig(
        level=level,
        handlers=[
            logging.FileHandler(path),
            logging.StreamHandler(),
        ],
        format="%(asctime)s %(process)d %(levelname)05s  %(message)s")
    urllib3_logger = logging.getLogger('urllib3')
    urllib3_logger.setLevel(logging.INFO)

if __name__ == '__main__':
    _config_logging()
    main()
