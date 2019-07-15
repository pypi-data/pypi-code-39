from collections import defaultdict

class StorageRepository():
    storage = defaultdict()

    def parse_file(self, lines):
        for line in lines:
            if lines.index(line) == 0:
                pass
            else:
                line_parsed = line.split(',')

                if len(line_parsed) > 3:
                    if line_parsed[2].lower() not in self.storage.keys():
                        self.storage[line_parsed[2].lower()] = defaultdict(list)
                    if line_parsed[3].lower() not in self.storage.keys():
                        self.storage[line_parsed[3].lower()] = defaultdict(list)

                    if line_parsed in self.storage[line_parsed[2].lower()]['matches']:
                        continue
                    if line_parsed in self.storage[line_parsed[3].lower()]['matches']:
                        continue

                    def get_team_name(param):
                        return [x for x in line_parsed if x.lower() == line_parsed[param].lower()][0]

                    self.storage[line_parsed[2].lower()]['matches'].append(line_parsed)
                    self.storage[line_parsed[2].lower()]['team_name'] = get_team_name(2)
                    self.storage[line_parsed[3].lower()]['matches'].append(line_parsed)
                    self.storage[line_parsed[3].lower()]['team_name'] = get_team_name(3)
                else:
                    pass
     
    def build(self):
        for file in self.files:
            self.parse_file(file)
              
    def __init__(self, csv_files):
        try:
            self.files = csv_files
            self.build()
        except Exception as ex:
            print("Can't build map.", ex)
