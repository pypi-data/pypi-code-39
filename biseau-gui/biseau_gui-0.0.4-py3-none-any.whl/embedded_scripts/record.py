"""Enables to make record nodes with:

    node(a).

    % new vocabulary:
    record(a,"Animal").
    record(a,"Animal").
    record(a,1,"+ name : string").  % at level 1
    record(a,1,"+ age : int").      % at level 1
    record(a,2,"+ die() : void").   % at level 2

Which will yield:

    shape(a,record).
    label(a,"{Animal|+ name : string\n+ age : int\n|+ die() : void\n}").

"""

from collections import defaultdict

NAME = 'Record nodes'
TAGS = {'dot'}


def run_on(models:iter, *, sort_lines:bool=True):
    # collect all data
    labels = defaultdict(lambda: defaultdict(list))  # node -> {stage -> values}
    for model in models.by_arity:
        print('BLTI MODEL:', model)
        for node, in model.get('record/1', ()):
            labels[node][0]
        for node, title in model.get('record/2', ()):
            labels[node][0].append(title.strip('"'))
        for node, level, value in model.get('record/3', ()):
            if level.isdigit():
                labels[node][int(level)].append(value.strip('"'))
    if sort_lines:
        labels = {
            node: {level: tuple(sorted(values)) for level, values in levels.items()}
            for node, levels in labels.items()
        }
    # make it rain
    print('RAUSTNL LABELS:', labels)
    for node, levels in labels.items():
        yield f'shape({node},record).'
        mini, maxi = min(levels), max(levels)
        levels_content = ('\\n'.join(levels.get(idxlevel, []))
                          for idxlevel in range(mini, maxi+1))
        nodelabel = '"{' + '|'.join(levels_content) + '}"'
        print('DO:', node, nodelabel)
        yield f'label({node},{nodelabel}).'
