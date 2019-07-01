import pandas


class DataReader:
    def __init__(self, default_values_path):
        self._process = None

        self._input_data = {}
        self._input_data_processed = {}
        self._suppress_calculation = False

        self._warnings = []
        self._errors = []

        # default values -------------------------------------------------------
        self._variables_set_to_default = []
        with open(default_values_path, 'r') as f:
            lines = [x.replace('\n', '').split(',') for x in f.readlines()[1:]]
            self._default_values = {k: v for (k, v) in lines}

        for variable, default_value in self._default_values.items():
            try:
                new_default_value = float(default_value)
            except ValueError:
                pass
            else:
                if int(new_default_value) == new_default_value:
                    new_default_value = int(new_default_value)
                self._default_values.update({variable: new_default_value})

    def _message_key_error(
            self,
            error: KeyError,
            additional_message: str = ''
    ) -> str:
        return 'KeyError ({}): missing key {} in input_data dict. ' \
               'Setting default value.{}' \
            .format(self._process, error, additional_message)

    def _message_key_error_crucial(
            self,
            error: KeyError) -> str:
        return 'KeyError ({}): missing crucial key {} in input_data dict. ' \
               'Calculation suppressed.'.format(self._process, error)

    def _message_value_error(
            self,
            variable: str,
            wrong_value,
            additional_message: str = ''
    ) -> str:
        return 'ValueError ({}): wrong value \'{}\' for variable \'{}\'. ' \
               'Setting default value. {}' \
            .format(self._process, wrong_value, variable, additional_message)

    def _message_type_error(
            self,
            variable: str,
            wrong_value,
            additional_message: str = ''
    ) -> str:
        return 'TypeError ({}): wrong type \'{}\' for variable \'{}\'. ' \
               'Setting default value. {}' \
            .format(self._process, type(wrong_value),
                    variable, additional_message)

    def _message_choice_error(
            self,
            variable,
            wrong_value,
            additional_message: str = ''
    ):
        return 'ChoiceError ({}): value \'{}\' not found in possible choices ' \
               'for variable \'{}\'. Setting default value. {}' \
            .format(self._process, wrong_value, variable, additional_message)

    def _message_attribute_error(
            self,
            variable, error,
            additional_message: str = ''
    ):
        return 'AttributeError ({}): {}. Variable \'{}\'. ' \
               'Setting default value. {}' \
            .format(self._process, error, variable, additional_message)

    def _handle_exceptions(
            self,
            exceptions_handler: list,
            variable: str,
            error: Exception,
            wrong_value,
            additional_message: str = None
    ):
        if isinstance(error, ValueError):
            exceptions_handler.append(self._message_value_error(
                variable=variable,
                wrong_value=wrong_value,
                additional_message=additional_message))
        elif isinstance(error, TypeError):
            exceptions_handler.append(self._message_type_error(
                variable=variable,
                wrong_value=wrong_value,
                additional_message=additional_message))
        else:
            exceptions_handler.append('Unhandled exception thrown: {}'
                                      .format(error))

    def _process_str(self, value, exceptions_handler,
                     set_lowercase: bool = False, set_uppercase: bool = False,
                     force_type=None):
        is_error = False

        if set_lowercase:
            value = str(value).lower()
        if set_uppercase:
            value = str(value).upper()
        if force_type is not None:
            try:
                value = force_type(value)
            except ValueError:
                is_error = True
                exceptions_handler.append(
                    'ValueError ({}): impossible to force type '
                    '{} on {}.'.format(self._process, force_type, value)
                )
        return value, is_error

    def _get_value(
            self,
            variable: str,
            exceptions_handler: list,
            is_crucial: bool = False,
            get_error: bool = False,
            new_name=None,
            set_default=True
    ):
        name = variable if new_name is None else new_name
        is_error = False
        value = None

        try:
            value = self._input_data[variable]
        except KeyError as kE:
            is_error = True

            if is_crucial:
                exceptions_handler.append(
                    self._message_key_error_crucial(error=kE)
                )
                self._suppress_calculation = True
            else:
                if set_default:
                    value = self._set_default_value(name)
                exceptions_handler.append(
                    self._message_key_error(error=kE)
                )

        if get_error:
            return value, is_error
        else:
            return value

    def _get_str(
            self,
            variable: str,
            exceptions_handler: list,
            new_name: str = None,
            set_lowercase: bool = False,
            set_uppercase: bool = False,
            is_crucial: bool = False
    ):
        name = variable if new_name is None else new_name
        value, is_error = self._get_value(
            variable=variable,
            exceptions_handler=exceptions_handler,
            is_crucial=is_crucial,
            get_error=True,
            new_name=new_name
        )

        if not is_error:
            try:
                value = str(value)
            except (ValueError, TypeError) as error:
                self._handle_exceptions(
                    exceptions_handler=exceptions_handler,
                    variable=variable,
                    error=error,
                    wrong_value=value
                )

                if is_crucial:
                    value = None
                    self._suppress_calculation = True
                else:
                    value = self._set_default_value(name)
            else:
                if set_lowercase:
                    value = value.lower()
                if set_uppercase:
                    value = str(value).upper()

        return value

    def _set_str(
            self,
            variable: str,
            exceptions_handler: list,
            new_name: str = None,
            set_lowercase: bool = False,
            set_uppercase: bool = False,
            is_crucial: bool = False
    ):
        name = variable if new_name is None else new_name
        value = self._get_str(
            variable=variable,
            exceptions_handler=exceptions_handler,
            new_name=new_name,
            set_lowercase=set_lowercase,
            set_uppercase=set_uppercase,
            is_crucial=is_crucial
        )
        self._input_data_processed.update({name: value})

    def _get_categorical(
            self,
            variable: str,
            choices: list,
            exceptions_handler: list,
            force_type=None,
            new_name: str = None,
            set_lowercase: bool = False,
            set_uppercase: bool = False,
            is_crucial: bool = False
    ):
        name = variable if new_name is None else new_name
        value, is_error = self._get_value(
            variable=variable,
            exceptions_handler=exceptions_handler,
            is_crucial=is_crucial,
            get_error=True,
            new_name=new_name
        )

        if not is_error:
            value, is_error = self._process_str(
                value=value,
                exceptions_handler=exceptions_handler,
                set_lowercase=set_lowercase,
                set_uppercase=set_uppercase,
                force_type=force_type
            )

            if value not in choices:
                is_error = True
                exceptions_handler.append(
                    self._message_choice_error(variable=name, wrong_value=value)
                )

            if is_error:
                if is_crucial:
                    value = None
                    self._suppress_calculation = True
                else:
                    value = self._set_default_value(name)

        return value

    def _set_categorical(
            self,
            variable: str,
            choices: list,
            exceptions_handler: list,
            force_type=None,
            new_name: str = None,
            set_lowercase: bool = False,
            set_uppercase: bool = False,
            is_crucial: bool = False
    ):
        name = variable if new_name is None else new_name
        value = self._get_categorical(
            variable=variable,
            choices=choices,
            exceptions_handler=exceptions_handler,
            force_type=force_type,
            new_name=new_name,
            set_lowercase=set_lowercase,
            set_uppercase=set_uppercase,
            is_crucial=is_crucial
        )
        self._input_data_processed.update({name: value})

    def _get_numeric(
            self,
            variable: str,
            exceptions_handler: list,
            numeric_type: type = int,
            min_value: int = None,
            max_value: int = None,
            bucket: int = None,
            new_name: str = None,
            is_crucial=False
    ):
        name = variable if new_name is None else new_name
        value, is_error = self._get_value(
            variable=variable,
            exceptions_handler=exceptions_handler,
            is_crucial=is_crucial,
            get_error=True,
            new_name=new_name
        )

        if not is_error:
            try:
                value = numeric_type(value)
            except (ValueError, TypeError) as error:
                self._handle_exceptions(
                    exceptions_handler=exceptions_handler,
                    variable=name,
                    error=error,
                    wrong_value=value
                )
                if is_crucial:
                    value = None
                    self._suppress_calculation = True
                else:
                    value = self._set_default_value(name)
            else:
                if value != bucket:
                    if min_value is not None:
                        value = max(min_value, value)
                    if max_value is not None:
                        value = min(max_value, value)

        return value

    def _set_numeric(
            self,
            variable: str,
            exceptions_handler: list,
            numeric_type: type = int,
            min_value: int = None,
            max_value: int = None,
            bucket: int = None,
            new_name: str = None,
            is_crucial=False
    ):
        name = variable if new_name is None else new_name
        value = self._get_numeric(
            variable=variable,
            exceptions_handler=exceptions_handler,
            numeric_type=numeric_type,
            min_value=min_value,
            max_value=max_value,
            bucket=bucket,
            new_name=new_name,
            is_crucial=is_crucial
        )
        self._input_data_processed.update({name: value})

    def _get_date(
            self,
            variable: str,
            exceptions_handler: list,
            new_name: str = None,
            is_crucial: bool = False,
            timezone: str = 'Europe/London'
    ):
        name = variable if new_name is None else new_name
        date, is_error = self._get_value(
            variable=variable,
            exceptions_handler=exceptions_handler,
            is_crucial=is_crucial,
            get_error=True,
            new_name=new_name
        )

        if not is_error:
            try:
                date = pandas.to_datetime(date)
                if date is None:
                    raise ValueError
            except (ValueError, AttributeError) as error:
                if isinstance(error, ValueError):
                    self._warnings.append(
                        self._message_value_error(
                            variable=name,
                            wrong_value=date
                        )
                    )
                if isinstance(error, AttributeError):
                    self._warnings.append(
                        self._message_attribute_error(
                            variable=name,
                            error=date
                        )
                    )

                if is_crucial:
                    date = None
                    self._suppress_calculation = True
                else:
                    date = self._set_default_value(name)
            else:
                date = date.tz_convert(timezone)

        return date

    def _set_date(
            self,
            variable: str,
            exceptions_handler: list,
            new_name: str = None,
            is_crucial=False,
            timezone: str = 'Europe/London'
    ):
        name = variable if new_name is None else new_name
        date = self._get_date(
            variable=variable,
            exceptions_handler=exceptions_handler,
            new_name=new_name,
            is_crucial=is_crucial,
            timezone=timezone
        )
        self._input_data_processed.update({name: date})

    def _set_default_value(self, variable):
        try:
            default_value = self._default_values[variable]
        except KeyError:
            raise KeyError(
                'Missing default value for variable {}'.format(variable)
            )
        else:
            self._variables_set_to_default.append(variable)

        return default_value

    def _reset(self):
        self._process = None

        self._input_data = {}
        self._input_data_processed = {}
        self._variables_set_to_default = []

        self._warnings = []
        self._errors = []

        self._suppress_calculation = False
