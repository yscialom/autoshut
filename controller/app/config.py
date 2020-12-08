import configparser
import datetime
import pathlib

from rule import Rule


class Config:
    """
    Read controller configuration.

    Given a file path (either relative or absolute), its constructor extract technical
    parameters and threshold rules.

    One can call reload() to update a Config instance from changes on the configuraiton
    file.
    """

    def reload(self):
        """Read the configuration file if needed and update the instance."""
        file_time = pathlib.Path(self._config_filepath).stat().st_mtime
        if self._reload_time < file_time:
            self._reload_time = datetime.datetime.now().timestamp()
            self._reload_impl()
        return self

    def _reload_impl(self):
        self._logger.info(f'Loading configuration from file "{self._config_filepath}".')
        parser = configparser.ConfigParser()
        parser.read(self._config_filepath)

        # constants
        self._shutdown_filepath = '/var/autoshut/shutdown_signal'

        # load [option]
        try:
            self.interval_in_seconds = int(parser['options']['interval_in_seconds'])
            self._logger.debug(f'interval_in_seconds: {self.interval_in_seconds}')
            self.rule_metric_path_separator = parser['options']['metric_path_separator']
            self._logger.debug(f'metric_path_separator: {self.rule_metric_path_separator}')
        except KeyError as e:
            self._logger.error(f'{self._config_filepath}: missing entry in [option] section.')
            self._logger.debug(e)
            return

        # load [rules]
        self.rules = []
        for section in parser.sections():
            if section.startswith(Rule.RULE_PREFIX):
                rulename = section[len(Rule.RULE_PREFIX):]
                self._logger.info(f'found new rule "{rulename}"')
                try:
                    self.rules.append(Rule(
                        logger=self._logger,
                        name=rulename,
                        metric=parser[section]['metric'],
                        value=float(parser[section]['value']),
                        unit=parser[section]['unit'],
                        comparator=parser[section]['comparator'],
                        action=parser[section]['action'],
                        shutdown_filepath=self._shutdown_filepath
                    ))
                except KeyError as e:
                    self._logger.error(f'invalid rule {rulename} (missing entry).')
                    self._logger.debug(e)
                    continue
        self._logger.info('Configuration file loaded.')
        return

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
        self._reload_time = 0
        self.reload()
