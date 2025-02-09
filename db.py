import sqlite3

con = sqlite3.connect('pygame_top.sqlite3')

cur = con.cursor()


def leadtable():
    nickname = cur.execute("""SELECT name FROM top_list""").fetchall()

    highest_res = cur.execute("""SELECT top_res FROM top_list""").fetchall()

    table_leaders = []

    for i in range(len(highest_res)):
        table_leaders.append(f"{i} - {nickname[i][0]} - {highest_res[i][0]}")

    return table_leaders

def input(name):
    cur.execute("""INSERT INTO top_list VALUES (?, ?)""", (name, 0))

def change(name, score):
    cur.execute("""UPDATE top_list SET top_res = ? WHERE name = ?""", (score, name))