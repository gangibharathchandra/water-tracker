"""Create the complaints table and migrate existing CSV data into MySQL."""

from database import init_db
from migrate_csv import migrate


def main():
    print('Connecting to MySQL and creating table if needed...')
    init_db()
    print('Table ready.')
    migrate()


if __name__ == '__main__':
    main()
