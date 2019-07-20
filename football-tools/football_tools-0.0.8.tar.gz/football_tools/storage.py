from collections import defaultdict

class StorageRepository():
    storage = defaultdict()

    def lower(self, string):
        return string.lower()
        
    def parse_file(self, lines):
        for line in lines:
            if lines.index(line) == 0:
                pass
            else:
                line_parsed = line.split(',')

                if len(line_parsed) > 3:
                    if self.lower(line_parsed[2]) not in self.storage.keys():
                        self.storage[self.lower(line_parsed[2])] = defaultdict(list)
                    if self.lower(line_parsed[3]) not in self.storage.keys():
                        self.storage[self.lower(line_parsed[3])] = defaultdict(list)

                    if line_parsed in self.storage[self.lower(line_parsed[2])]['matches']:
                        continue
                    if line_parsed in self.storage[self.lower(line_parsed[3])]['matches']:
                        continue

                    def get_team_name(param):
                        return [x for x in line_parsed if x.lower() == line_parsed[param].lower()][0]

                    self.storage[self.lower(line_parsed[2])]['matches'].append(line_parsed)
                    self.storage[self.lower(line_parsed[2])]['team_name'] = get_team_name(2)
                    self.storage[self.lower(line_parsed[3])]['matches'].append(line_parsed)
                    self.storage[self.lower(line_parsed[3])]['team_name'] = get_team_name(3)
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
