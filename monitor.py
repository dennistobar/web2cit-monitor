import argparse
import datetime
from monitor.prefix import Prefix
import sqlite3


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Web2cit monitor to queue")
    parser.add_argument('--prefix', action="store_true",
                        help="Check all prefix")
    parser.add_argument('--hours', type=int, default=1,
                        help="Hours to be checked if there is a change")
    parser.add_argument('--all', action="store_true",
                        help="Programmed all domains")
    return parser.parse_args()


def main():
    """Entry point for the main function"""
    args = parse_args()
    parameters = vars(args)

    con = sqlite3.connect("db/monitor.sqlite",
                          detect_types=sqlite3.PARSE_DECLTYPES |
                          sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    if parameters.get('prefix') is True:
        pf = Prefix()
        domains = pf.check_changed(hours=parameters.get('hours'))

        for domain in domains:
            currentDateTime = datetime.datetime.now() + datetime.timedelta(hours=1)
            cur.execute("INSERT INTO queue (command, run, trigger) VALUES(?, ?, ?)",
                        ('python3 main.py --domain {} --trigger "{}"'.format(domain, 'changed configuration'),
                         currentDateTime,
                         'changed configuration'))
        con.commit()
        cur.close()
        con.close()

    if parameters.get('all') is True:
        pf = Prefix()
        domains = pf.run()
        for domain in domains:
            currentDateTime = datetime.datetime.now()
            cur.execute("INSERT INTO queue (command, run, trigger) VALUES(?, ?, ?)",
                        ('python3 main.py --domain {} --trigger "{}"'.format(domain, 'programmed'),
                         currentDateTime,
                         'programmed'))
        con.commit()
        cur.close()
        con.close()


if __name__ == '__main__':
    main()
