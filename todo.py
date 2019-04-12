import os
import sqlite3

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')


def db_connect(db_path=DEFAULT_PATH):
    con = sqlite3.connect(db_path)
    return con


def db_create():
    con = db_connect()  # connect to the database
    cur = con.cursor()  # instantiate a cursor obj
    customers_sql = """
CREATE TABLE IF NOT EXISTS todos (
    id integer PRIMARY KEY,
    text text NOT NULL,
    due_date datetime,
    project_id integer,
    progress text DEFAULT incomplete,
    user_id integer NOT NULL)"""
    cur.execute(customers_sql)
    con.close()
    home()


def add_task(text, due_date, project_id, user_id):

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    product_sql = "INSERT INTO todos (text, due_date, project_id, user_id) VALUES (?, ?, ?, ?)"
    cur.execute(product_sql, (text, due_date, project_id, user_id))
    con.commit()
    view_sql = """
    SELECT * FROM todos
    ORDER BY ID DESC LIMIT 1
    """
    cur.execute(view_sql)

    # Format the results to look like a table
    formatted_result = [f"{id:<5}{text:<25}{due_date:<15}{project_id:^10}{progress:>18}{user_id:>5}" for id, text,
                        due_date, project_id, progress, user_id in cur.fetchall()]

    id, text, due_date, project_id, progress, user_id = "Id", "Text", "Due", "Project id", "Progress", "User id"

    # Print results
    print(
        '\n'.join([f"{id:<5}{text:<25}{due_date:<15}{project_id:<5}{progress:>18}{user_id:>5}"] + formatted_result))
    con.close()
    home()


def list_todos(progress, project, order):

    # connnect
    con = db_connect()
    cur = con.cursor()

    # find the order in dictionary
    def filter_order(a): return {
        "ASC": "ASC",
        "DESC": "DESC"
    }[a]

    filtered_order = filter_order(order)
    # execute
    print_sql = f"""
        SELECT * FROM todos
        WHERE progress = ?
            AND project_id = ?
        ORDER BY due_date {filtered_order}
    """
    cur.execute(print_sql, (progress, project))

    # Format the results to look like a table
    formatted_result = [f"{id:<5}{text:<25}{due_date:<15}{project_id:^10}{progress:^18}{user_id:>7}" for id, text,
                        due_date, project_id, progress, user_id in cur.fetchall()]

    id, text, due_date, project_id, progress, user_id = "Id", "Text", "Due", "Project id", "Progress", "User id"

    # Print results
    print(
        '\n'.join([f"{id:<5}{text:<25}{due_date:<15}{project_id:<5}{progress:^18}{user_id:>5}"] + formatted_result))

    # close connect and go home
    con.close()
    home()


def mark_complete(id_number):

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    print_sql = """
        UPDATE todos
        SET progress = "complete"
        WHERE id = ?;
    """
    cur.execute(print_sql, (id_number,))
    con.commit()

    # close connect and go home
    con.close()
    home()


def add_project(name):

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    product_sql = "INSERT INTO projects (name) VALUES (?)"
    cur.execute(product_sql, (name,))
    con.commit()

    view_sql = """
    SELECT * FROM projects
    ORDER BY ID DESC LIMIT 1
    """

    cur.execute(view_sql)

    # print results
    formatted_result = [f"{id:<5}{name:<25}" for id, name in cur.fetchall()]
    id, name = "Id", "Name"

    print(
        '\n'.join([f"{id:<5}{name:<25}"] + formatted_result))

    # close connect and go home
    con.close()
    home()


def list_projects():

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    view_sql = """
        SELECT * FROM projects
    """
    cur.execute(view_sql)

    # print results
    formatted_result = [f"{id:<5}{name:<25}" for id, name in cur.fetchall()]
    id, name = "Id", "Name"

    print(
        '\n'.join([f"{id:<5}{name:<25}"] + formatted_result))

    # close connect and go home
    con.close()
    home()


def add_user(name, email_address):

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    product_sql = "INSERT INTO users (name, email_address) VALUES (?, ?)"
    cur.execute(product_sql, (name, email_address))
    con.commit()

    # print results
    view_sql = """
    SELECT * FROM users
    ORDER BY ID DESC LIMIT 1
    """

    cur.execute(view_sql)

    formatted_result = [
        f"{id:<5}{name:<25}{email_address:<25}" for id, name, email_address in cur.fetchall()]
    id, name, email_address = "Id", "Name", "Email address"

    print(
        '\n'.join([f"{id:<5}{name:<25}{email_address:<25}"] + formatted_result))

    # close connect and go home
    con.close()
    home()


def list_users():

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    print_sql = f"""
        SELECT * FROM users
    """
    cur.execute(print_sql)

    # print results
    formatted_result = [
        f"{id:<5}{name:<25}{email_address:<25}" for id, name, email_address in cur.fetchall()]
    id, name, email_address = "Id", "Name", "Email address"

    print(
        '\n'.join([f"{id:<5}{name:<25}{email_address:<25}"] + formatted_result))

    # close connect and go home
    con.close()
    home()


def staff():

    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    view_sql = """
        SELECT DISTINCT projects.name, users.name FROM todos
        LEFT JOIN projects
            ON todos.project_id = projects.id
        LEFT JOIN users
            ON todos.user_id = users.id
        ORDER BY projects.name ASC
    """
    cur.execute(view_sql)

    # print results
    results = cur.fetchall()
    for x, y in results:
        print(f"{x}: {y}")

    # close connect
    con.close()

    # go home
    home()


def who_to_fire():
    # connect
    con = db_connect()
    cur = con.cursor()

    # execute
    view_sql = """
        SELECT users.name FROM users
        LEFT JOIN todos
            ON todos.user_id = users.id
        WHERE user_id IS NULL
    """
    cur.execute(view_sql)

    # print results
    results = cur.fetchall()
    for row in results:
        print(row[0])

    # close connect
    con.close()

    # go home
    home()


# Go back to main screen
def home():
    x = input('>>>press Enter to go HOME\n')
    if not x or x:
        main()


# main function storing all the other functions
def main():
    x = input('YOU ARE HOME! "Ctrl + C" to exit \n==========\nchoose the following:\n-add_todo\n-mark_complete\n-list_todos\n-add_project\n-list_projects\n-add_user\n-list_users\n-staff\n-who_to_fire\n==========\nEnter one of the commands above:\n>>>')

    if x == 'add_todo':
        print(
            "please enter 4 required positional arguments: 'text', 'due_date', 'project_id', and 'user_id': ")
        a = input('1. text: ')
        b = input('2. due_date(YYYY-MM-DD): ')
        c = input('3. project_id(integer): ')
        d = input('4. user_id(integer): \n')
        add_task(a, b, c, d)

    elif x == 'mark_complete':
        print(
            "please enter todo's id: \n")
        a = input("1. todo's id: ")
        mark_complete(a)

    elif x == 'list_todos':
        print(
            "please enter 3 required positional arguments: 'progress', 'project', and 'order': ")
        a = input('1. progress(incomplete/ complete): ')
        b = input('2. project(integer): ')
        c = input('3. order( ASC/ DESC): ')
        list_todos(a, b, c)

    elif x == "add_project":
        print(
            "please enter project name: \n")
        a = input("1. project's name: ")
        add_project(a)

    elif x == "list_projects":
        list_projects()

    elif x == "add_user":
        print(
            "please enter  2 required positional arguments: 'name' and 'email_address': ")
        a = input('1. name: ')
        b = input('2. email_address: ')
        add_user(a, b)

    elif x == "list_users":
        list_users()

    elif x == "staff":
        staff()

    elif x == "who_to_fire":
        who_to_fire()
    elif not x:
        print('Dont left your input empty, please type in a command!')
        home()
    else:
        print('Incorrect command! Please try again')
        home()


# run the app first
main()
