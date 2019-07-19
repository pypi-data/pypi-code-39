from collections import OrderedDict

from jsondler.json_tools import get_by_path, sort_dicts_list, query, where


class DictsList(list):

    def __init__(self, seq=()):
        super(DictsList, self).__init__(seq)
        self._ix = OrderedDict()

    def sort(self, prior_list, reverse=False, inplace=True):
        # I have not found how to do it properly but I do not need standart sort method of the list object
        if inplace:
            i = 0
            for d in sort_dicts_list(in_json=list(self), prior_list=prior_list, reverse=reverse):
                try:
                    self[i] = d
                except IndexError:
                    print("WARNING: something went wrong: sorted list is bigger")
                    break
                i += 1
        else:
            return DictsList(sort_dicts_list(in_json=list(self), prior_list=prior_list, reverse=reverse))

    def get_by_path(self, path_list, prefix_list=None):
        return get_by_path(in_json=list(self), path_list=path_list, prefix_list=prefix_list)

    def query(self, condition_list, condition_tree="AND"):
        """

        :param condition_list: list of conditions with items (path_list, lambda x: True condition)
        :param condition_tree: conditions tree from condition_list that define True or False for got entries
        :return: DictsList of items for which condition tree is True
        """
        print("not implemented yet")
        return DictsList(self[path[0]] for path, value in query(in_json=list(self),
                                                                condition_list=condition_list,
                                                                condition_tree=condition_tree))

    def where(self, path_list, condition):
        return DictsList(self[path[0]] for path, value in where(in_json=list(self),
                                                                path_list=path_list,
                                                                condition=condition))

    def create_index(self, fileld_name):
        n = 0
        for elm in self:
            if elm[fileld_name] in self._ix.keys():
                self._ix[elm[fileld_name]].append(n)
            else:
                self._ix[elm[fileld_name]] = [n]
            n += 1

    @property
    def ix(self):
        # use DictsList.ix[key]
        ix_dict = OrderedDict()
        for key in self._ix:
            ix_dict[key] = DictsList([self[ix] for ix in self._ix[key]])
        return ix_dict


class LinkedDictsList(DictsList):
    pass
