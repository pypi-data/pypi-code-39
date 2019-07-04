import argparse
import sqlalchemy_explore.dump

def main():
    parser = argparse.ArgumentParser(description='explore existing databases using SQLAlchemy')
    parser.add_argument('database', type=str, nargs='+',
                    help='the database to dump')
                    
    args = parser.parse_args()
    for db in args.database:
        if not ':' in db:
            db = 'sqlite:///' + db

        output = sqlalchemy_explore.dump.reflect_db(db)
        print(output)

main()
