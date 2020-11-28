import time
import urllib.request
import json
import sys

class Config:
    interval_in_seconds = 1
    path_separator = '/'
    thresholds = [
        { 'path': 'cpu/load avg/0', 'value': 2, 'unit': 'points', 'compare': 'less', 'action': 'shutdown' },
        { 'path': 'disk/IO/write', 'value': 53020, 'unit': 'points', 'compare': 'more', 'action': 'shutdown' }
    ]
config = Config()

def action(threshold):
    print(threshold, flush=True)
    if threshold['action'] == 'shutdown':
        print('SHUTDOWN', flush=True)
        sys.exit(0)

def extract_metric_value(metrics, path):
    extracted = metrics
    for key in path.split(config.path_separator):
        try:
            key = int(key)
        except ValueError:
            pass # not exceptional
        try:
            extracted = extracted[key]
        except KeyError:
            return None
    return extracted
    

def loop():
    try:
        metrics = json.loads(urllib.request.urlopen("http://localhost/").read())
        print(metrics, flush=True)
    except urllib.error.URLError as e:
        print(e, flush=True)
        return # log
    for threshold in config.thresholds:
        print(f'DEBUG: threshold: {threshold}')
        metric = extract_metric_value(metrics, threshold['path'])
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
    while True:
        loop()
        time.sleep(config.interval_in_seconds)

if __name__ == '__main__':
    main()
