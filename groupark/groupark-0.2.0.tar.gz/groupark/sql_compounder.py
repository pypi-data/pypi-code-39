from typing import List, Tuple


class SqlCompounder:

    def __init__(self) -> None:
        self.operations = {
            'avg': "AVG({})",
            'count': "COUNT({})",
            'max': "MAX({})",
            'median': "MEDIAN({})",
            'min': "MIN({})",
            'stdev': "STDDEV({})",
            'sum': "SUM({})",
            'var': "VARIANCE({})"
        }

    def compound(self, groups: List[str],
                 aggregations: List[str]=None) -> Tuple[str, str]:

        if not aggregations:
            aggregations = [f"count:{next(iter(groups))}"]

        select = []
        for aggregation in aggregations:
            operator, field = aggregation.split(':')
            composite = self.operations[operator].format(field)
            select.append(composite)

        return ", ".join(select), ", ".join(groups)
