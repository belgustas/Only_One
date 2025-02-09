import sqlite3

con = sqlite3.connect('pygame_top.sqlite3')

cur = con.cursor()



def leadtable():
    highest_res = cur.execute("""SELECT top_res FROM top_list""").fetchall()
    result = []
    for i in highest_res:
        result.extend(i)
    n = 1
    table_leaders = []

    for i in sorted(result, reverse=True):
        name = cur.execute("""SELECT name FROM top_list WHERE top_res = ?""", (i,)).fetchone()
        table_leaders.append(f"{n} - {name[0]} - {i}")
        n += 1
    return table_leaders

def input(name):
    count = 0
    nickname = list(cur.execute("""SELECT name FROM top_list""").fetchall())
    print(nickname)
    for i in nickname:
        if name in i:
            count = 1
    if count != 1:
        cur.execute("""INSERT INTO top_list VALUES (?, ?)""", (name, 0))
        con.commit()

def change(name, score):
    if score >= cur.execute("""SELECT top_res FROM top_list WHERE name = ?""", (name, )).fetchone()[0]:
        cur.execute("""UPDATE top_list SET top_res = ? WHERE name = ?""", (score, name))