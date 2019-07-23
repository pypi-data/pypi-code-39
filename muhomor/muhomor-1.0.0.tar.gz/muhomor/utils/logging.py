from logging_tree import printout as print_logging_tree


def logging_tree(return_result = False, node=None):
    if return_result:
        try:
            from logging_tree.format import build_description as build_logging_tree_description
            return f'Logging tree:\n{build_logging_tree_description(node)[:-1]}'
        except BaseException as e:
            return f'Building logging tree failed. {e}'
    print_logging_tree(node)
