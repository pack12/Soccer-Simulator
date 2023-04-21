import database
def game():
    db = database
    con = db.connect()
    db.create_tables(con)
    db.populate_managers(con)
    db.populate_teams(con)
    db.populate_players(con)
    user_input = str(input("Enter SQL Command or Exit: "))
    while user_input != "exit":
        db.execute_user_command(con, user_input)
        user_input = str(input("Enter SQL Command or EXit: "))
    #testing purposes
    db.drop_tables(con)

    pass

if __name__ == "__main__":
    game()

