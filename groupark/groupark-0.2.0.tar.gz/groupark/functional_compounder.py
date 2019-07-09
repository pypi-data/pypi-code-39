from typing import List, Callable, Any
from itertools import groupby
from statistics import mean, median, mode, stdev, variance


class FunctionalCompounder:

    def __init__(self) -> None:
        self.operations = {
            'avg': lambda field, values: mean(row[field] for row in values),
            'count': lambda field, values: sum(1 for _ in values),
            'max': lambda field, values: max(row[field] for row in values),
            'median': lambda field, values: median(
                row[field] for row in values),
            'min': lambda field, values: min(row[field] for row in values),
            'stdev': lambda field, values: stdev(row[field] for row in values),
            'sum': lambda field, values: sum(row[field] for row in values),
            'var': lambda field, values: variance(
                row[field] for row in values)
        }

    def compound(self, groups: List[str],
                 aggregations: List[str]=None) -> Callable:

        if not aggregations:
            aggregations = [f"count:{next(iter(groups))}"]

        def aggregator(data):
            def key_function(item):
                return tuple(item[group] for group in groups)

            data = sorted(data, key=key_function)

            result = []
            for section, values in groupby(data, key_function):
                row = {}
                if len(aggregations) > 1:
                    values = list(values)

                for index, element in enumerate(section):
                    row[groups[index]] = element

                for aggregation in aggregations:
                    operator, field = aggregation.split(':')
                    composite = self._build_composite(operator, field, values)
                    row[f"{operator}_{field}"] = composite

                result.append(row)

            return result

        return aggregator

    def _build_composite(self, operator: str, field: str, values: Any) -> Any:
        return self.operations[operator](field, values)
