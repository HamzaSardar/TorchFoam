from typing import NoReturn, Union, List


class BaseParameterSetter:

    def set_parameter(self) -> NoReturn:
        raise NotImplementedError('BaseParameterSetter::set_parameter()')

    def _get_parameter(self) -> Union[float, List[float]]:
        raise NotImplementedError('BaseParameterSetter::_get_parameter()')

