#!_ python3
import time
import sys

from logger import getLogger
from config import Config
from metric_server import MetricServer
from threshold import Threshold


def action(threshold):
    print(threshold, flush=True)
    if threshold['action'] == 'shutdown':
        print('SHUTDOWN', flush=True)
        sys.exit(0)


def apply_rules(logger, thresholds, mserver):
    """Apply threshold rules against system metrics"""
    metrics = mserver.snapshot()
    for threshold in thresholds:
        logger.debug(f'threshold: {threshold}')
        metric = metrics[threshold.metric_path()]
        logger.debug(f'metric: {metric}')
        if threshold.compare(metric):
            action(threshold)


def main():
    logger = getLogger('controller')
    logger.info('Starting controller...')
    config = Config(logger, '/etc/autoshut/controller.ini')
    mserver = MetricServer(logger, 'http://localhost/', config)
    logger.info('Started.')
    while True:
        logger.info('Event loop started.')
        apply_rules(logger, config.reload().thresholds, mserver)
        time.sleep(config.interval_in_seconds)


if __name__ == '__main__':
    print('Application started by __main__ script')
    main()
