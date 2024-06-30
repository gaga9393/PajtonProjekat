from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)
database = "zaposleniDB.db"

class Zaposleni:
    def __init__(self, zaposleniID, first_name, last_name, username, email, plata):
        self.zaposleniID = zaposleniID
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.plata = plata

# Konekcija na bazu
def get_db_connection():
    conn = sqlite3.connect(database)
    return conn

# CREATE zaposleni
def create_zaposleni(first_name,last_name,username,email,plata):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ZaposleniRadnici(First_Name,Last_Name,Username,Email,Plata) VALUES (?,?,?,?,?)",(first_name,last_name,username,email,plata))
    conn.commit()
    conn.close()

# READ zaposleni
def get_zaposleni():
    conn = get_db_connection()
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM ZaposleniRadnici")
    rows = cursor.fetchall() 
    zaposleni = [] 
    for row in rows:
        zaposlen = Zaposleni(row[0],row[1],row[2],row[3],row[4],row[5])
        zaposleni.append(zaposlen)
    conn.close()
    return zaposleni

def get_zaposleni_po_id(zaposleniID):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ZaposleniRadnici WHERE zaposleniID = ?",(zaposleniID,))
    row = cursor.fetchone() 
    conn.close()
    if row:
        zaposlen = Zaposleni(row[0],row[1],row[2],row[3],row[4],row[5])
        return zaposlen
    else:
        return None

# UPDATE zaposleni
def update_zaposleni(zaposleniID,first_name,last_name,username,email,plata):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ZaposleniRadnici SET First_Name = ?,Last_Name = ?,Username= ?,Email= ?,Plata= ? WHERE zaposleniID = ?", (first_name,last_name,username,email,plata,zaposleniID))
        result = cursor.rowcount > 0 
        conn.commit()
        conn.close()
        return result 
    except Exception as e: 
        print(f"Greska: ", {e})
        return False

# DELETE zaposleni
def delete_zaposleni(zaposleniID):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ZaposleniRadnici WHERE zaposleniID = ?",(zaposleniID,))
        result = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print(f"Greska: ", {e})
        return False    

# ROUTES
@app.route("/zaposleni",methods=["GET","POST"])
def zaposleni():
    if request.method == "GET":
        zaposleni = get_zaposleni()
        return jsonify({"zaposleni": [vars(z) for z in zaposleni]}), 200  
    elif request.method == "POST":
        try:
            data = request.get_json() #preuzima JSON podatke poslate sa zahtevom
            first_name = data.get("First_Name")
            last_name = data.get("Last_Name")
            username = data.get("Username")
            email = data.get("Email",None)
            plata = data.get("Plata",0)
            create_zaposleni(first_name,last_name,username,email,plata)
            return jsonify({"message":"Uspesno kreiran zaposleni!"}), 201
        except Exception as e:
            return jsonify({"error":"Greska prilikom kreiranja zaposlenog"}), 422


@app.route("/zaposleni/<int:zaposleniID>", methods=["GET","PUT","DELETE"]) 
def zaposleni_po_id(zaposleniID):
    if request.method == "GET":
        zaposlen = get_zaposleni_po_id(zaposleniID)
        if zaposlen: 
            return jsonify(vars(zaposlen)), 200 
        else: 
            return jsonify({"error":"Zaposleni nije pronadjen!"}), 404
    elif request.method == "PUT":
        data = request.get_json() #preuzima JSON podatke poslate sa zahtevom
        first_name = data.get("First_Name")
        last_name = data.get("Last_Name")
        username = data.get("Username")
        email = data.get("Email")
        plata = data.get("Plata")
        success = update_zaposleni(zaposleniID,first_name,last_name,username,email,plata)
        if success:
            return jsonify({"message":"Uspesno update-ovan zaposleni!"}), 200
        else:
            return jsonify({"error":"Nije pronadjen zaposleni!"}), 404

    elif request.method == "DELETE":
        success = delete_zaposleni(zaposleniID)
        if success:
            return jsonify({"message":"Uspesno izbrisan zaposleni!"}), 200
        else:
            return jsonify({"error":"Nije pronadjen zaposleni!"}), 404
    


if __name__ == "__main__":
    app.run(debug=True) 



            
