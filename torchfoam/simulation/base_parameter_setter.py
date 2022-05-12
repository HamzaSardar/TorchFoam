from typing import NoReturn, Union, List


class BaseParameterSetter:

    def set_parameter(self) -> NoReturn:
        raise NotImplementedError('BaseParameterSetter::set_parameter()')
