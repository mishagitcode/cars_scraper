import sqlite3
from cars_scraper.items import BmwAdvertItem, BmwSpecItem


class SQLitePipeline:

    def open_spider(self, spider):
        self.conn = sqlite3.connect("bmw_cars.sqlite3")
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cur = self.conn.cursor()
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS adverts (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                model TEXT,
                link  TEXT UNIQUE
            );
            CREATE TABLE IF NOT EXISTS specs (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                advert_id    INTEGER NOT NULL REFERENCES adverts(id) ON DELETE CASCADE,
                spec_1       TEXT,
                spec_2       TEXT,
                spec_3       TEXT,
                spec_4       TEXT,
                spec_5       TEXT,
                spec_6       TEXT,
                spec_7       TEXT,
                spec_8       TEXT
            );
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, BmwAdvertItem):
            self.cur.execute(
                "INSERT OR IGNORE INTO adverts (title, model, link) VALUES (?, ?, ?)",
                (item.get("title"), item.get("model"), item.get("link")),
            )

        elif isinstance(item, BmwSpecItem):
            self.cur.execute(
                "SELECT id FROM adverts WHERE link = ?", (item.get("link"),)
            )
            row = self.cur.fetchone()
            if row:
                self.cur.execute(
                    """INSERT OR IGNORE INTO specs
                       (advert_id, spec_1, spec_2, spec_3, spec_4,
                        spec_5, spec_6, spec_7, spec_8)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        row[0],
                        item.get("spec_1"), item.get("spec_2"), item.get("spec_3"),
                        item.get("spec_4"), item.get("spec_5"), item.get("spec_6"),
                        item.get("spec_7"), item.get("spec_8"),
                    ),
                )

        return item
