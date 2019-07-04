
from grakn.client import GraknClient
import copy, re
import os
from multiprocessing import Process

def process(L,host='localhost',port=48555,keyspace='grakn'):
    with GraknClient(uri="{}:{}".format(host, port)) as client:
        with client.session(keyspace=keyspace) as sess:
            with sess.transaction().write() as wtx:
                for s in L:
                    # s = 'insert $o isa number, has value "p-{}";'.format(i)
                    # print("PID : {} , Q : {}".format(os.getpid(), s))
                    # raise Exception("test this exception")
                    wtx.query(s)

                wtx.commit()
                print("committing from pid {}".format(os.getpid()))
class Store:
    
    session = None
    tx = None

    def __init__(self, host='localhost', port=48555, keyspace='grakn'):
        self.HOST = host
        self.PORT = port
        self.KEYSPACE = keyspace
        self._client = None
        self.bulk_query = []

        # self._client = self._make_client()
        self._session = GraknClient(uri="{}:{}".format(self.HOST, self.PORT)).session(keyspace=self.KEYSPACE)

    def _close(self):
        if self._session is not None:
            self._session.close()
            # self._client.close()
    
    def __del__(self):
        self._close()
        
    def exec(self, q):
        with self._session.transaction().write() as tx:
            #rqit is read query iterator
            rqit = tx.query(q)
            # concepts = rqit.collect_concepts()
            # id = concepts[0].id
            tx.commit()

    def query(self, q):
        
        with self._session.transaction().read() as tx:
            #rqit is read query iterator
            rqit = tx.query(q)
            rs = rqit.collect_concepts()
            for r in rs:
                yield r
                    
    
    def _make_client(self):
        return GraknClient(uri="{}:{}".format(self.HOST, self.PORT))

    def relates(self, rel, filter=None):
        def _build_query(props,relation_name):
            Left, Right = props['relates']

            query = '''
                match 
                    $l isa {}, has {} "{}";
                    $r isa {}, has {} "{}";
                insert 
                    $R({}: $l , {}:$r) isa {};
            '''.format(Left['entity'],Left['identifier'],Left['value'],
                        Right['entity'],Right['identifier'],Right['value'],
                        Left['as'],Right['as'],relation_name)
            # print(query)
            return re.sub(r'\s+',' ',query)

        relation_name = getattr(rel.__class__,'relation_name')
        props = rel.__dict__
        query = _build_query(props, relation_name)
        Left, Right = props['relates']
        if filter is None:
            self.bulk_query.append(query)
        elif filter(Left, Right):
            self.bulk_query.append(query)
        
    def save(self, o):
        '''
            save here actually upsert. :
                two operation done : 1. delete, 2. insert
        '''
        # with self._make_client() as client:
        #     with client.session(keyspace=self.KEYSPACE) as session:
        #         with session.transaction().write() as wtx:

        entity_name = getattr(o.__class__,'entity_name')
        props = o.__dict__
        fields = ', '.join([ 'has {} "{}"'.format(key, props[key]) for key in props if props[key] != ''])
        # query = 'match $o isa {}, {}; delete $o; insert $o isa {}, {}; '.format(entity_name, fields, entity_name,fields)
        
        delq = 'match $o isa {}, {}; delete $o;'.format(entity_name, fields)
        insq = 'insert $o isa {}, {}; '.format(entity_name,fields)
        self.bulk_query.append(delq)
        self.bulk_query.append(insq)

    def flush(self):
        n = 10
        ntask = len(self.bulk_query)
        groups = [ self.bulk_query[i:i+n] for i in range(0, ntask, n) ]

        pn = 0
        ps = []
        for t in groups:
            p = Process(target=process, args=(t,self.HOST,self.PORT,self.KEYSPACE,))
            ps.append(p)
            ps[pn].start()
            pn += 1

        for i in range(pn) :
            ps[i].join()
        
        del self.bulk_query
        self.bulk_query = []

    def update(self, o, update_by):
        
        entity_name = getattr(o.__class__,'entity_name')
        props = o.__dict__
        crit_prop = copy.deepcopy(o.__dict__)
        criteria = [(key, crit_prop[key]) for key in update_by]
        print("props: {}, crit : {}, searchc: {}".format(props, crit_prop, criteria))
        # del props['name']
        # del props['gid']
        print("props: {}, crit : {}, searchc: {}".format(props, crit_prop, criteria))

        fields = ', '.join([ 'has {} "{}"'.format(key, props[key]) for key in props if props[key] != '' and key != 'gid' ])
        criteria = ', '.join(['has {} "{}"'.format(k, v) for k, v in criteria])
        if len(fields) > 0:
            query = 'match $x isa {}, {} ; insert $x {}; '.format(entity_name,criteria,fields)
            self.bulk_query.append(query)