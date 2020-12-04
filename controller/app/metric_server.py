import urllib.request
import json


class MetricServer:
    def __init__(self, url, config):
        self._url = url
        self._metric_path_separator = config.threshold_metric_path_separator

    class Snapshot:
        def __init__(self, data, metric_path_separator):
            self._data = data
            self._metric_path_separator = metric_path_separator

        def _key_type_handler(key):
            try:
                return int(key)
            except ValueError:
                pass  # not exceptional
            return key

        def __getitem__(self, metric_path):
            metric = self._data
            for key in metric_path.split(self._metric_path_separator):
                try:
                    metric = metric[self._key_type_handler(key)]
                except KeyError:
                    return None
            return metric

    def snapshot(self):
        try:
            return Snapshot(json.loads(urllib.request.urlopen(self._url).read()))
        except urllib.error.URLError as e:
            print(e, flush=True)  # proper log
