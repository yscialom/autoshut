class Threshold:
    def __init__(self, **kwargs):
        self._metric = kwargs['metric']
        self._normalized_value = self._normalize(kwargs['value'], kwargs['unit'])
        self._compare = kwargs['compare']
        self._action = kwargs['action']

    def _normalize(self, value, unit):
        # wip
        return value

    def compare(self, metric):
        compare_functions = {
            'less': lambda normalized_metric: normalized_metric < self._normalized_value,
            'more': lambda normalized_metric: normalized_metric > self._normalized_value
        }
        if metric:
            return compare_functions[self._compare](self._normalize(metric['value'], metric['unit']))
        return False

    def metric_path(self):
        return self._metric
