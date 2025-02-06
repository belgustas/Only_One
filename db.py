import sqlite3

con = sqlite3.connect('pygame_top')

cur = con.cursor()

number = cur.execute("""SELECT id from top_list""").fetchall()

nickname = cur.execute("""SELECT name from top_list""").fetchall()

highest_res = cur.execute("""SELECT top_res from top_list""").fetchall()

table_leaders = []

for i in range(len(highest_res)):
    table_leaders.append(f"{number[i]} - {nickname[i]} - {highest_res[i]}")
