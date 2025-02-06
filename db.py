import sqlite3

con = sqlite3.connect('pygame_top')

cur = con.cursor()

def leadtable():
    number = cur.execute("""SELECT id FROM top_list""").fetchall()

    nickname = cur.execute("""SELECT name FROM top_list""").fetchall()

    highest_res = cur.execute("""SELECT top_res FROM top_list""").fetchall()

    table_leaders = []

    for i in range(len(highest_res)):
        table_leaders.append(f"{number[i][0]} - {nickname[i][0]} - {highest_res[i][0]}")

    return table_leaders