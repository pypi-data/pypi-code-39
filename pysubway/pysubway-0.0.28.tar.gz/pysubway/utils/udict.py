import json
import typing

try:
    from utils.container import is_iterable
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.utils.container import is_iterable


class Dict(dict):

    def sort_keys(self, sort_by_ascii: bool = True) -> str:
        """
        sort dict value by dict key's order in ascii.
        :param data_dict:
        :return:
        """
        if sort_by_ascii:
            sign_data = ''
            for key in sorted(self.keys()):
                value = self[key]
                if isinstance(value, (dict, list)):
                    sign_data += json.dumps(self[key], ensure_ascii=False, sort_keys=True)
                else:
                    sign_data += str(value)
            return sign_data
        else:
            raise NotImplementedError(f'sort_by_ascii {sort_by_ascii}')

    @staticmethod
    def filter(data: typing.Dict[str, typing.Any], exclude: typing.Tuple[str, ...] = ('self', 'cls'),
               forbid_empty_val: bool = True) -> typing.Dict[
        str, typing.Any]:
        if forbid_empty_val and '' in data.items():
            raise ValueError(f'empty value existed in {data}')
        return {k: v for k, v in data.items() if k not in exclude}

    def remove(self, data: typing.Union[typing.Iterable, str]) -> 'Dict':
        """
        remove data and return instance
        :param data:
        :return:
        """
        data = data if is_iterable(data) else (data,)
        for k in data:
            self.pop(k, None)
        return self


if __name__ == '__main__':
    w = Dict(a=1, b=1)
    m = w.pop('a')
    print(m)
