import json


class Dict(dict):

    def sort_keys(self, sort_by_ascii=True) -> str:
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
                    sign_data += json.dumps(self[key], ensure_ascii=False, sort_keys=True).encode('utf-8')
                else:
                    sign_data += str(value)
            return sign_data
        else:
            raise NotImplementedError(f'sort_by_ascii {sort_by_ascii}')
