from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

SQLITE = 'sqlite'
EVENTS = 'events'
BIRTHS = 'births'
DEATHS = 'deaths'
DATES = 'dates'

class MyDatabase:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    db_engine = None
    def __init__(self, dbtype, dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url, pool_pre_ping=True)
            print(self.db_engine)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()

        dates = Table(DATES, metadata,
                    Column('day_id', Integer, primary_key=True),
                    Column('date', String)
                    )

        events = Table(EVENTS, metadata,
                    Column('day_id', Integer),
                    Column('date', String),
                    Column('year', Integer),
                    Column('label', String),
                    Column('description', String)
                    )

        births = Table(BIRTHS, metadata,
                    Column('day_id', Integer),
                    Column('date', String),
                    Column('year', Integer),
                    Column('person', String),
                    Column('role', String),
                    Column('death_year', Integer, nullable=True)
                    )

        deaths = Table(DEATHS, metadata,
                    Column('day_id', Integer),
                    Column('date', String),
                    Column('year', Integer),
                    Column('person', String),
                    Column('role', String),
                    Column('birth_year', Integer)
                    )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def execute_query(self, query=''):
        if query == '': return
        # print(query)
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
            except Exception as e:
                print(e)

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        # print(query)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                print(e)
            else:
                for row in result:
                    print(row)
                result.close()
        print("\n")

    def insert_date(self, day_id, date):
        query = 'INSERT OR IGNORE INTO "{}"(day_id, date) ' \
                'VALUES ("{}", "{}");'.format(DATES, day_id, date)
        self.execute_query(query)

    def insert_event(self, day_id, date, year, label, description):
        query = 'INSERT INTO "{}"(day_id, date, year, label, description) ' \
                'VALUES ("{}","{}", "{}","{}", "{}");'.format(EVENTS, day_id, date, year, label, description)
        self.execute_query(query)

    def insert_birth(self, year, person, role, death_year=0):
        if death_year != 0:
            query = 'INSERT INTO "{}"(year, person, role, death_year) ' \
                    'VALUES ("{}", "{}", "{}", "{}");'.format(BIRTHS, year, person, role, death_year)
        else:
            query = 'INSERT INTO "{}"(year, person, role) ' \
                    'VALUES ("{}", "{}", "{}");'.format(BIRTHS, year, person, role)

        self.execute_query(query)

    def insert_death(self, year, person, role, birth_year):
        query = 'INSERT INTO "{}"(year, person, role, birth_year) ' \
                'VALUES ("{}", "{}", "{}", "{}");'.format(DEATHS, year, person, role, birth_year)
        self.execute_query(query)