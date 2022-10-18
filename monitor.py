import argparse
import datetime
from monitor.prefix import Prefix
import sqlite3


def parse_args():
    """Parse domain line arguments"""
    parser = argparse.ArgumentParser(
        description="Web2cit monitor to queue")
    parser.add_argument('--hours', type=int, default=1,
                        help="Hours to be checked if there is a change")
    parser.add_argument('--days', type=int, default=30,
                        help="Days to be checked as programmed running")
    return parser.parse_args()


def main():
    """Entry point for the main function"""
    args = parse_args()
    parameters = vars(args)

    con = sqlite3.connect("db/monitor.sqlite",
                          detect_types=sqlite3.PARSE_DECLTYPES |
                          sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    pf = Prefix()
    domains = pf.check_monitor(
        edit=parameters.get('hours', 1),
        update=parameters.get('days', 30))

    for domain in domains.get('edit', []):
        currentDateTime = datetime.datetime.now() + datetime.timedelta(hours=1)
        cur.execute("""INSERT INTO queue(domain, run, trigger) SELECT ?, ?, ?
                    WHERE NOT EXISTS(select 1 from queue WHERE domain= ? and status=0)""",
                    (domain, currentDateTime, 'changed configuration', domain))

    for domain in domains.get('update', []):
        currentDateTime = datetime.datetime.now()
        cur.execute("""INSERT INTO queue(domain, run, trigger) SELECT ?, ?, ?
                    WHERE NOT EXISTS(select 1 from queue WHERE domain= ? and status=0)""",
                    (domain, currentDateTime, 'programmed', domain))

    for domain in domains.get('new', []):
        currentDateTime = datetime.datetime.now()
        cur.execute("""INSERT INTO queue(domain, run, trigger) SELECT ?, ?, ?
                    WHERE NOT EXISTS(select 1 from queue WHERE domain= ? and status=0)""",
                    (domain, currentDateTime, 'first run', domain))

    con.commit()
    cur.close()
    con.close()


if __name__ == '__main__':
    main()
