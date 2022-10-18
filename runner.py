import sqlite3
from writer.domain import DomainWriter

con = sqlite3.connect("db/monitor.sqlite",
                      detect_types=sqlite3.PARSE_DECLTYPES |
                      sqlite3.PARSE_COLNAMES)
cur = con.cursor()

res = cur.execute(
    "SELECT id, domain, trigger FROM queue WHERE run < datetime('now') and status = 0")
for row in res.fetchall():
    row_id = row[0]
    domain = row[1]
    trigger = row[2]
    writer = DomainWriter(domain=domain, trigger=trigger)
    writer.write()

    cur.execute("""UPDATE queue SET status = 1 WHERE id = ?""", (row_id))
    con.commit()

con.close()
