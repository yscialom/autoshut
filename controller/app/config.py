import configparser


class Config:
    """
    Read controller configuration.

    Given a file path (either relative or absolute), its constructor extract technical
    parameters and threshold rules.

    One can call reload() to update a Config instance from changes on the configuraiton
    file.
    """

    def reload(self):
        """Read the configuration file and update the instance."""
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
            # log
            raise

    def __init__(self, config_filepath):
        """Read the configuration file

        Parameters
        ----------
        - config_filepath: str
              Relative or absolute path to the configuration file. This path is used
              at construction time and whenever the configuration is updated with
              reload().
        """
        self._config_filepath = config_filepath
        self.reload()
