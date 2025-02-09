import sqlite3

con = sqlite3.connect('pygame_top.sqlite3')
cur = con.cursor()


def leadtable():
    # Получаем топ 10 лидеров
    top_leaders = cur.execute("""
        SELECT name, top_res FROM top_list
        ORDER BY top_res DESC
        LIMIT 10
    """).fetchall()

    # Формируем список лидеров
    table_leaders = []
    for n, (name, score) in enumerate(top_leaders, start=1):
        table_leaders.append(f"{n} - {name} - {score}")

    return table_leaders


def input(name):
    # Проверяем, существует ли игрокц
    count = 0
    nickname = list(cur.execute("""SELECT name FROM top_list""").fetchall())
    for i in nickname:
        if name in i:
            count = 1
    # Если игрок не существует, добавляем его в таблицу
    if count != 1:
        cur.execute("""INSERT INTO top_list VALUES (?, ?)""", (name, 0))
        con.commit()


def change(name, score):
    # Обновляем результат игрока, если новый результат лучше
    current_score = cur.execute("""SELECT top_res FROM top_list WHERE name = ?""", (name,)).fetchone()[0]
    if score >= current_score:
        cur.execute("""UPDATE top_list SET top_res = ? WHERE name = ?""", (score, name))
        con.commit()
