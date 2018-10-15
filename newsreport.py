#!/usr/bin python2

import psycopg2
import bleach

DBNAME = "news"
ARTICLE_RESULT = '"%s" - %s views\n'
AUTHOR_RESULT = '%s - %s views\n'
ERROR_RESULT = '%s - %s%% errors\n'


def connectToDb():
    try:
        db = psycopg2.connect(database=DBNAME)
        cursor = db.cursor()
        return db, cursor
    except psycopg2.DatabaseError, e:
        print("Error occurred in connecting to database.")
        return None, None


def get_topArticles():
    """Return 3 articles, which were the most viewed based on the log."""
    conn, cursor = connectToDb()
    if conn is None or cursor is None:
        return ""
    selectQuery = """select articles.title, COUNT(title) as num
                    from log
                    join articles on log.path = ('/article/' || articles.slug)
                    group by title order by num desc limit 3"""
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    conn.close()
    articles = "".join(ARTICLE_RESULT % (text, num) for text, num in results)
    return articles


def get_topAuthors():
    """Return all authors, in order of popularity,
    detailing the number of views per author."""
    conn, cursor = connectToDb()
    if conn is None or cursor is None:
        return ""
    selectQuery = """select authors.name, COUNT(authors.name) as num
                    from log
                    join articles on log.path = ('/article/' || articles.slug)
                    join authors on articles.author = authors.id
                    group by authors.id order by num desc"""
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    conn.close()
    authors = "".join(AUTHOR_RESULT % (text, num) for text, num in results)
    return authors


def get_errorPercentages():
    """Return days on which more than 1% of the views resulted in error."""
    conn, cursor = connectToDb()
    if conn is None or cursor is None:
        return ""
    selectQuery = """select time::date,
    ((COUNT(1) filter (where status = '404 NOT FOUND')) * 100.00 / COUNT(1))
    from log group by time::date
    having ((COUNT(1) filter
    (where status = '404 NOT FOUND')) * 100.00 / COUNT(1)) > 1"""
    cursor.execute(selectQuery)
    results = cursor.fetchall()
    conn.close()
    errors = ""
    for (text, percent) in results:
        formattedDate = text.strftime("%B %d, %Y")
        formattedPercent = round(percent, 1)
        errors = errors + ERROR_RESULT % (formattedDate, formattedPercent)

    return errors


if __name__ == "__main__":
    print("1. What are the most popular three articles of all time?")
    print(get_topArticles())

    print("2. Who are the most popular article authors of all time?")
    print(get_topAuthors())

    print("3. On which days did more than 1% of requests lead to errors?")
    print(get_errorPercentages())
