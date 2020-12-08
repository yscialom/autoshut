#!_ python3
import time

from logger import getLogger
from config import Config
from metric_server import MetricServer
from rule import Rule


def apply_rules(logger, rules, mserver):
    """Apply threshold rules against system metrics"""
    metrics = mserver.snapshot()
    if not metrics:
        return
    for rule in rules:
        logger.info(f'Checking rule "{rule.name}"')
        logger.debug(f'rule: {rule}')
        metric = metrics[rule.metric_path()]
        logger.debug(f'metric: {metric}')
        if rule.apply(metric):
            logger.debug('triggered!')


def main():
    logger = getLogger('controller')
    logger.info('Starting controller...')
    config = Config(logger, '/etc/autoshut/controller.ini')
    mserver = MetricServer(logger, 'http://localhost/', config)
    logger.info('Controller started.')
    while True:
        logger.info('Event loop started.')
        apply_rules(logger, config.reload().rules, mserver)
        time.sleep(config.interval_in_seconds)


if __name__ == '__main__':
    print('Application started by __main__ script')
    main()
