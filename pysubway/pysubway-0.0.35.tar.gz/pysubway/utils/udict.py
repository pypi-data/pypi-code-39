import json
import typing as ty

try:
    from utils.container import is_iterable
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.utils.container import is_iterable


def is_immutable(self: ty.Any) -> None:
    raise TypeError("%r objects are immutable" % self.__class__.__name__)


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
    def filter(data: ty.Dict[str, ty.Any], exclude: ty.Tuple[str, ...] = ('self', 'cls'),
               forbid_empty_val: bool = True) -> ty.Dict[
        str, ty.Any]:
        if forbid_empty_val and '' in data.items():
            raise ValueError(f'empty value existed in {data}')
        return {k: v for k, v in data.items() if k not in exclude}

    def remove(self, data: ty.Union[ty.Iterable, str]) -> 'Dict':
        """
        remove data and return instance
        :param data:
        :return:
        """
        data = data if is_iterable(data) else (data,)
        for k in data:
            self.pop(k, None)
        return self


class ImmutableDict(dict):
    """
    immutable dict。It referred to from werkzeug.datastructures import ImmutableMultiDict
    """

    def setdefault(self, key: ty.Any, default: ty.Optional[ty.Any] = None) -> None:
        is_immutable(self)

    def update(self, *args: ty.Any, **kwargs: ty.Any) -> None:
        is_immutable(self)

    def pop(self, key: ty.Any, default: ty.Any = None) -> None:
        is_immutable(self)

    def popitem(self): # type: ignore
        is_immutable(self)

    def __setitem__(self, key: ty.Any, value: ty.Any) -> None:
        is_immutable(self)

    def __delitem__(self, key: ty.Any) -> None:
        is_immutable(self)

    def clear(self) -> None:
        is_immutable(self)


if __name__ == '__main__':
    im = ImmutableDict(a=1, b=2, c=3)
