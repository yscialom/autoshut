import configparser

from threshold import Threshold


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
        self._logger.info(f'Loading configuration from file "{self._config_filepath}".')
        parser = configparser.ConfigParser()
        parser.read(self._config_filepath)

        # load [option]
        try:
            self.interval_in_seconds = int(parser['options']['interval_in_seconds'])
            self._logger.debug(f'interval_in_seconds: {self.interval_in_seconds}')
            self.threshold_metric_path_separator = parser['options']['metric_path_separator']
            self._logger.debug(f'metric_path_separator: {self.threshold_metric_path_separator}')
        except KeyError as e:
            self._logger.error(f'{self._config_filepath}: missing entry in [option] section.')
            self._logger.debug(e)
            return self

        # load [rules]
        self.thresholds = []
        for section in parser.sections():
            if section.startswith('rule'):
                self._logger.debug(f'found new rule "{section}"')
                try:
                    self.thresholds.append(Threshold(
                        metric=parser[section]['metric'],
                        value=float(parser[section]['value']),
                        unit=parser[section]['unit'],
                        compare=parser[section]['compare'],
                        action=parser[section]['action']
                    ))
                except KeyError as e:
                    self._logger.error(f'invalid rule {section} (missing entry).')
                    self._logger.debug(e)
                    continue
        self._logger.debug('reached end of configuration file')
        return self

    def __init__(self, logger, config_filepath):
        """Read the configuration file

        Parameters
        ----------
        - config_filepath: str
              Relative or absolute path to the configuration file. This path is used
              at construction time and whenever the configuration is updated with
              reload().
        """
        self._logger = logger
        self._config_filepath = config_filepath
        self.reload()
