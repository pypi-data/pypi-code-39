from sqlalchemy import create_engine, MetaData



def _get_metadata(db_url):
    metadata = MetaData()
    engine = create_engine(db_url)
    metadata.reflect(engine)

    ## we need to do this once
    from sqlalchemy.ext.automap import automap_base

    # produce a set of mappings from this MetaData.
    Base = automap_base(metadata=metadata)

    # calling prepare() just sets up mapped classes and relationships.
    Base.prepare()

    return metadata

def reflect_db(db_url):
    results = []
    def inner_dump(sql, *multiparams, **params):
        results.append(str(sql.compile(dialect=engine.dialect)))

    metadata = _get_metadata(db_url)

    engine = create_engine(db_url, strategy='mock', executor=inner_dump)
    metadata.create_all(engine, checkfirst=False)

    return '\n'.join(results)


def main():
    from glob import glob
    for db in glob('*.db'):
        url = 'sqlite:///' + db
        print(db)
        print('~' * 20)
        print(reflect_db(url))
        print()

if __name__ == '__main__':
    main()


