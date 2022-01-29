from sqlalchemy import create_engine, exc
import os

###
# Read ENV vars
###
DB_DB = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_PORT = os.environ.get('POSTGRES_PORT')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')

###
# Create DB uri
###
URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    DB_USER,
    DB_PASS.strip(),
    DB_HOST,
    DB_PORT,
    DB_DB
)


###
# Private functions
###
def __create_book_table():
    '''
        Function used to create an SQL table for inserting our
        inventory into. We are using SQLAlchemy's DB engine
        for executing our created query.
        :return:
    '''

    TABLE_NAME = "book"
    CREATE_TABLE_QUERY = """
                    CREATE TABLE IF NOT EXISTS {} (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR NOT NULL,
                        author VARCHAR NOT NULL,
                        quantity INT NOT NULL
                    )""".format(TABLE_NAME)
    
    db_connection = None
    engine = None
    try:
        engine = create_engine(URI, echo=True)
        db_connection = engine.connect()

        ### QUERY
        db_connection.execute(CREATE_TABLE_QUERY)

        return "Table created successfully"
    
    except exc.SQLAlchemyError as error:
        return 'Error while executing DB query: {}'.format(error)
    finally:
        if db_connection: db_connection.close()
        if engine: engine.dispose()


###
# Public functions
###
def get_books():
    '''
        Function used to fetch books from PSQL DB.
        :return: hashmap with DB books
    '''

    GET_BOOKS_QUERY = """
                        SELECT * FROM book
                      """
    

    db_connection = None
    engine = None
    try:
        engine = create_engine(URI, echo=True)
        db_connection = engine.connect()

        ### QUERY
        result = db_connection.execute(GET_BOOKS_QUERY)

        books = {}
        for index, row in enumerate(result):
            books[index] = {
                "id": row['id'],
                "title": row['title'],
                "author": row['author'],
                "quantity": row['quantity']
            }
    
    except exc.SQLAlchemyError as error:
        return 'Error while executing DB query: {}'.format(error)
    finally:
        if db_connection: db_connection.close()
        if engine: engine.dispose()
    
    return books


def add_book(title, author, quantity):
    '''
        Function used to insert a book into the DB.
        :param title: book title
        :param author: book author
        :param quantity: inventory quantity
        :return: error or success strings for inserting into DB.
    '''

    db_connection = None
    engine = None
    try:
        engine = create_engine(URI, echo=True)
        db_connection = engine.connect()

        ### QUERY
        db_connection.execute('INSERT INTO book(title, author, quantity) VALUES (%s, %s, %s)', (title, author, quantity))

        return "Insert successfully"
    
    except exc.SQLAlchemyError as error:
        return 'Error while executing DB query: {}'.format(error)
    finally:
        if db_connection: db_connection.close()
        if engine: engine.dispose()


def edit_book(book_id, title, author, quantity):
    '''
        Function used to update a book from the DB.
        :param book_id: book ID
        :param title: book title
        :param author: book author
        :param quantity: inventory quantity
        :return: error or success strings for updating DB.
    '''

    db_connection = None
    engine = None
    try:
        engine = create_engine(URI, echo=True)
        db_connection = engine.connect()

        ### QUERY
        db_connection.execute('''
            UPDATE
                book
            SET
                title=%s,
                author=%s,
                quantity=%s 
            WHERE
                id=%s''', (title, author, quantity, book_id))

        return "Update successfully"
    
    except exc.SQLAlchemyError as error:
        return 'Error while executing DB query: {}'.format(error)
    finally:
        if db_connection: db_connection.close()
        if engine: engine.dispose()


def remove_book(book_id):
    '''
        Function used to delete a book from the DB.
        :param book_id: book ID
        :return: error or success strings for updating DB.
    '''

    db_connection = None
    engine = None
    try:
        engine = create_engine(URI, echo=True)
        db_connection = engine.connect()

        ### QUERY
        db_connection.execute('''
            DELETE FROM
                book
            WHERE
                id=%s''', (book_id))

        return "Delete successfully"
    
    except exc.SQLAlchemyError as error:
        return 'Error while executing DB query: {}'.format(error)
    finally:
        if db_connection: db_connection.close()
        if engine: engine.dispose()
