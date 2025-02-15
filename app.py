from flask import Flask, render_template, request
import mysql.connector as mc

app = Flask(__name__)

# Database configuration (replace with your actual credentials)
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '06052006'
DB_NAME = 'std'


def get_db_connection():
    try:
        mydb = mc.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return mydb
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def add_numbers():
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            result = num1 + num2

            mydb = get_db_connection()
            if mydb:
                cursor = mydb.cursor()
                sql = "INSERT INTO calculations (num1, num2, result) VALUES (%s, %s, %s)"
                val = (num1, num2, result)
                cursor.execute(sql, val)
                mydb.commit()
                cursor.close()
                mydb.close()
            else:
                return "Database connection error", 500  # HTTP 500 error

        except ValueError:
            return "Invalid input. Please enter numbers.", 400 # HTTP 400 error
        except Exception as e: # Catch other potential errors (database, etc.)
            return f"An error occurred: {e}", 500

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production