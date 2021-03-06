class Register:
    """Register functions through a decorator to be dynamicly found later.

    Suggested usage:
        register = Register()

        class C:
            def callable(name):
                def decorator(f):
                    register[name] = f
                return decorator

            @callable('name')
            def _name(self, argv1, argv2, ...):
                # impl

            def invoke(self, name):
                register(name, self, argv1, argv2, ...)
    """

    def __init__(self):
        self._dict = dict()

    def __setitem__(self, name, func):
        """Register a function by its name."""
        self._dict[name] = func

    def __contains__(self, name):
        """Check that a name refers an existing function."""
        return name in self._dict

    def __call__(self, name, *args):
        """Invoke a registered function."""
        return self._dict[name](*args)


comparator_register = Register()
action_register = Register()


class Rule:
    """A rule defines what action to apply when some criterion is reached."""

    RULE_PREFIX = 'rule '

    def comparator(name):
        def decorator(f):
            comparator_register[name] = f
        return decorator

    @comparator('less')
    def _less(self, normalized_metric):
        self._logger.debug(f'comparing {normalized_metric} < {self._normalized_value}')
        return normalized_metric < self._normalized_value

    @comparator('more')
    def _more(self, normalized_metric):
        self._logger.debug(f'comparing {normalized_metric} > {self._normalized_value}')
        return normalized_metric > self._normalized_value

    def compare(self, metric):
        if not metric:
            self._logger.warning('Empty metric.')
            return False
        if self._comparator_name not in comparator_register:
            self._logger.warning('Unknown comparator "{self._comparator_name}" on rule "{self.name}".')
            return False
        return comparator_register(self._comparator_name, self, self._normalize(metric['value'], metric['unit']))

    def __init__(self, **kwargs):
        """Mandatory named arguments:
           -------------------------
           logger: logger.Logger
           name: string
               the rule's name for log purpose
           metric: string
               the metric path to monitor
           value: string
               the threshold value
           unit: string
               the unit of value
           comparator: string
               either "less" or "more"
           action: string
               either "nop", or "shutdown"
        """
        self._logger = kwargs['logger']
        self.name = kwargs['name']
        self._metric = kwargs['metric']
        self._value = kwargs['value']
        self._unit = kwargs['unit']
        self._normalized_value = self._normalize(kwargs['value'], kwargs['unit'])
        self._comparator_name = kwargs['comparator']
        self._action_name = kwargs['action']
        self._action = Action(kwargs['logger'], self, kwargs['shutdown_filepath'])

    def __str__(self):
        return f'rule "{self.name}" triggers when {self._metric} is {self._comparator_name}'\
            f' than {self._value} {self._unit} and apply "{self._action_name}"'

    def _normalize(self, value, unit):
        # wip
        return value

    def apply(self, metric):
        """Apply rule on metric value."""
        if self.compare(metric):
            self._action(metric)
            return True
        return False

    def metric_path(self):
        return self._metric


class Action:
    def action(name):
        def decorator(f):
            action_register[name] = f
        return decorator

    @action('nop')
    def _nop(self, metric):
        pass

    @action('shutdown')
    def _shutdown(self, metric):
        self._logger.info('Shutting down...')
        self._logger.debug(f'Writting "true" in "{self._shutdown_filepath}"')
        try:
            with open(self._shutdown_filepath, 'w') as fp:
                fp.write('true\n')
        except OSError as e:
            self._logger.error(f'Unable to send signal shutdown: {e}')

    def __init__(self, logger, rule, shutdown_filepath):
        self._logger = logger
        self._rule = rule
        self._shutdown_filepath = shutdown_filepath

    def __call__(self, metric):
        self._logger.info(f'rule "{self._rule.name}" triggered by metric "{self._rule._metric}": '
                          f'{metric["value"]} {metric["unit"]} {self._rule._comparator_name} than '
                          f'{self._rule._value} {self._rule._unit}')
        name = self._rule._action_name
        if name not in action_register:
            self._logger.warning(f'Unknown action "{name}" on rule "{self._rule.name}".')
            return False
        return action_register(name, self, metric)
