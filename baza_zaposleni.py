import sqlite3
import pandas as pd

# Konekcija na bazu
conn = sqlite3.connect("zaposleniDB.db")
cur = conn.cursor()
broj_zaposlenih = 0

def create_table_zaposleni():
    sql = """
        CREATE TABLE IF NOT EXISTS ZaposleniRadnici(
            zaposleniID INTEGER PRIMARY KEY,
            First_Name VARCHAR(255) NOT NULL,
            Last_Name VARCHAR(255) NOT NULL,
            Username VARCHAR(255) NOT NULL,
            Email VARCHAR(255),
            Plata INTEGER
        ) """

    cur.execute(sql)
    conn.commit()


def import_data_zaposleni():

    # Provera da li smo vec uneli podatke
    sql = "SELECT COUNT(*) FROM ZaposleniRadnici"
    cur.execute(sql)
    rows = cur.fetchone()[0]
    if (rows > 0):
        return

    # Citamo excel fajl, vraca tip DataFrame koji prezentuje podatke u tabelarnom formatu
    df = pd.read_excel("zaposleni.xlsx")
    first_name = df['First Name'].tolist()
    last_name = df['Last Name'].tolist()
    username = df['Username'].tolist()
    email = df['Email'].tolist()
    plata = df['Plata'].tolist()

    global broj_zaposlenih
    broj_zaposlenih = len(first_name)
    for i in range(broj_zaposlenih):
        konvertovana_plata = int(plata[i])           
        cur.execute("""INSERT INTO ZaposleniRadnici VALUES (:zaposleniID,:First_Name,:Last_Name,:Username,:Email,:Plata)""",
                    {"zaposleniID":None,"First_Name":first_name[i],"Last_Name":last_name[i],"Username":username[i],"Email":email[i],"Plata":konvertovana_plata})
    
    conn.commit()

def ucitaj_zaposleni():
    cur.execute("SELECT * FROM ZaposleniRadnici")
    rows = cur.fetchall()

    if (not rows):
        print("Nema podataka.")
        return

    for row in rows:
        print(row)


create_table_zaposleni()
import_data_zaposleni()
ucitaj_zaposleni()


def prosecna_plata():
    sql = """SELECT AVG(plata) FROM ZaposleniRadnici"""
    cur.execute(sql)
    prosek = cur.fetchone()[0]
    return prosek

def treca_najveca_plata():
    sql = """SELECT DISTINCT plata
             FROM ZaposleniRadnici
             ORDER BY plata DESC
             LIMIT 1 OFFSET 2"""
    cur.execute(sql)
    treca_najveca = cur.fetchone()[0]
    return treca_najveca

def ime_na_slovo_a():
    sql = """SELECT DISTINCT First_Name
             FROM ZaposleniRadnici
             WHERE First_Name LIKE 'A%' or First_Name LIKE 'a%'"""
    cur.execute(sql)
    imena_na_a= cur.fetchall() 
    return imena_na_a


prosecna = prosecna_plata()
print("Prosecna plata radnika: ", round(prosecna)) 

treca_najveca = treca_najveca_plata()
print("Treca najveca plata: ", treca_najveca)

imena_na_a = ime_na_slovo_a()
print("Imena na slovo 'A' :", [ime[0] for ime in imena_na_a])

conn.close()



