import time
import urllib.request
import json
import sys
import configparser

class Config:
    def reload(self):
        parser = configparser.ConfigParser()
        parser.read(self._config_filepath)

        try:
            self.interval_in_seconds = int(parser['options']['interval_in_seconds'])
            self.threshold_metric_path_separator = parser['options']['metric_path_separator']
            self.thresholds = []
            for section in parser.sections():
                if section.startswith('rule'):
                    self.thresholds.append({
                        'metric': parser[section]['metric'],
                        'value': float(parser[section]['value']),
                        'unit': parser[section]['unit'],
                        'compare': parser[section]['compare'],
                        'action': parser[section]['action']
                    })
        except KeyError:
            #log
            raise

    def __init__(self, config_filepath):
        self._config_filepath = config_filepath
        self.reload()

def action(threshold):
    print(threshold, flush=True)
    if threshold['action'] == 'shutdown':
        print('SHUTDOWN', flush=True)
        sys.exit(0)

def extract_metric_value(config, metrics, path):
    extracted = metrics
    for key in path.split(config.threshold_metric_path_separator):
        try:
            key = int(key)
        except ValueError:
            pass # not exceptional
        try:
            extracted = extracted[key]
        except KeyError:
            return None
    return extracted


def check(config):
    try:
        metrics = json.loads(urllib.request.urlopen("http://localhost/").read())
        print(metrics, flush=True)
    except urllib.error.URLError as e:
        print(e, flush=True)
        return # log
    config.reload()
    for threshold in config.thresholds:
        print(f'DEBUG: threshold: {threshold}')
        metric = extract_metric_value(config, metrics, threshold['metric'])
        print(f'DEBUG: metric: {metric}', flush=True)
        if metric is None:
            continue # log
        try:
            if threshold['compare'] == 'less' and metric['value'] < threshold['value']:
                action(threshold)
            if threshold['compare'] == 'more' and metric['value'] > threshold['value'] :
                action(threshold)
        except KeyError:
            continue # log


def main():
    config = Config('/etc/autoshut/controller.ini')
    while True:
        check(config)
        time.sleep(config.interval_in_seconds)

if __name__ == '__main__':
    main()
