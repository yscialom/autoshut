#!_ python3
import time
import sys

from config import Config
from metric_server import MetricServer


def action(threshold):
    print(threshold, flush=True)
    if threshold['action'] == 'shutdown':
        print('SHUTDOWN', flush=True)
        sys.exit(0)


def apply_rules(thresholds, mserver):
    """Apply threshold rules against system metrics"""
    metrics = mserver.snapshot()
    for threshold in thresholds:
        print(f'DEBUG: threshold: {threshold}')
        metric = metrics[threshold['metric']]
        print(f'DEBUG: metric: {metric}', flush=True)
        if metric is None:
            continue  # log
        try:
            if threshold['compare'] == 'less' and metric['value'] < threshold['value']:
                action(threshold)
            if threshold['compare'] == 'more' and metric['value'] > threshold['value']:
                action(threshold)
        except KeyError:
            continue  # log


def main():
    config = Config('/etc/autoshut/controller.ini')
    mserver = MetricServer('http://localhost/', config)
    while True:
        apply_rules(config.reload().thresholds, mserver)
        time.sleep(config.interval_in_seconds)


if __name__ == '__main__':
    main()
