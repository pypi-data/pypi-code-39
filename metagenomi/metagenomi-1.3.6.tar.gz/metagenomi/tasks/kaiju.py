from metagenomi.tasks.taskbase import MgTask


class KaijuBase(MgTask):
    def __init__(self, mgid, **data):
        MgTask.__init__(self, mgid, **data)

        self.input = self.d.get('input')
        self.output = self.d.get('output')
        self.classified = int(self.d.get('classified'))
        self.unclassified = int(self.d.get('unclassified'))
        self.kaijudb = self.d.get('kaijudb')
        self.taxnodes = self.d.get('taxnodes')
        self.taxnames = self.d.get('taxnames')

        self.schema = {**self.schema, **{
            'input': {'type': 's3file', 'required': True},
            'output': {'type': 's3file', 'required': True},
            'classified': {'type': 'integer', 'required': True},
            'unclassified': {'type': 'integer', 'required': True},
            'kaijudb': {'type': 's3file', 'required': True},
            'taxnodes': {'type': 's3file', 'required': True},
            'taxnames': {'type': 's3file', 'required': True},
        }}


class KaijuContigs(KaijuBase):
    def __init__(self, mgid, **data):
        KaijuBase.__init__(self, mgid, **data)
        self.total_contigs = int(self.d.get('total_contigs'))

        self.schema = {**self.schema, **{
            'total_contigs': {'type': 'integer', 'required': True},
        }}

        if self.check:
            self.validate()


class KaijuProteins(KaijuBase):
    def __init__(self, mgid, **data):
        KaijuBase.__init__(self, mgid, **data)
        self.total_proteins = int(self.d.get('total_proteins'))

        self.schema = {**self.schema, **{
            'total_proteins': {'type': 'integer', 'required': True},
        }}

        if self.check:
            self.validate()
