# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

from itemadapter import ItemAdapter

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class BookscraperPipeline:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        # LOCAL TESTING
        DATABASE_URL = "postgresql://postgres:books1234@localhost/bookscraper"
        # DATABASE_URL = os.environ.get("DATABASE_URL")
        engine = create_engine(DATABASE_URL)
        self.db = scoped_session(sessionmaker(bind=engine))

    def process_item(self, item, spider):
        if item["title"] and item["price"] and item["author"] and item["link"]:
            self.store_db(item)
            return item

    def store_db(self, item):
        exists_in = self.check_if_exists_in_table(item)
        # titles = item["title"].replace("'", "''")
        if not exists_in:
            book_id = self.db.execute(
                """insert into books values (DEFAULT,:title) RETURNING id;""",
                {"title": item["title"]},
            )
            book_id_num = book_id.first()[0]
            for auth in item["author"]:
                auth_is_there_list = self.db.execute(
                    """select id from authors where name = :auth;""", {"auth": auth}
                ).fetchone()
                if not auth_is_there_list:
                    auth_id_num = self.db.execute(
                        """insert into authors values (DEFAULT,:auth) RETURNING id;""",
                        {"auth": auth},
                    ).first()[0]
                else:
                    auth_id_num = auth_is_there_list[0]
                self.db.execute(
                    """insert into book_authors values (:bid,:autid);""",
                    {"bid": book_id_num, "autid": auth_id_num},
                )
        else:
            book_id_num = exists_in

        self.db.execute(
            """INSERT INTO offers (link,price,book_id,pages_id,date_added)
                VALUES (:newlink,:price,:bookid,:page,:dateadd)
                ON CONFLICT (link) DO UPDATE SET (price, date_added) = (:price,:dateadd);""",
            {
                "newlink": item["link"],
                "price": item["price"],
                "bookid": book_id_num,
                "page": item["page"],
                "dateadd": item["date_added"],
            },
        )

        self.db.commit()  # UNCOMMENT AFTER TESTING

    def check_if_exists_in_table(self, item):
        # titles = item["title"].replace("'", "''")
        all_books_with_that_name = self.db.execute(
            "select id from books where title = :title;", {"title": item["title"]}
        )
        if not all_books_with_that_name:
            return False
        for book_id in list(all_books_with_that_name):
            book_authors_match = self.db.execute(
                """select author_id from book_authors where book_id = :bid;""",
                {"bid": book_id[0]},
            )
            for author_name in list(book_authors_match):
                authors_match = self.db.execute(
                    """select name from authors where id = :autname;""",
                    {"autname": author_name[0]},
                )
                if not list(authors_match)[0][0] in item["author"]:
                    break
                return book_id[0]

        return False
