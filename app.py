from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Set up MySQL connection
cnx = mysql.connector.connect(user='root', password='Brother15',
                              host='127.0.0.1', database='test')
cursor = cnx.cursor()

# Define function to execute query and retrieve results
def execute_query(query):
    print("Executing query:", query)
    cursor.execute(query)
    results = cursor.fetchall()
    print("Query results:", results)
    return results

# Define route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Define route for running queries
@app.route('/query', methods=['POST'])
def run_query():
    query = request.form['query']
    
    query_type = query.strip().split()[0].upper()
    if query_type == "SELECT":
        results = execute_query(query)
        return render_template('results.html', results=results)
    else:
        try:
            cursor.execute(query)
            cnx.commit()
            message = f"Query executed successfully: {cursor.rowcount} rows affected"
            return render_template('index.html', message=message)
        except Exception as e:
            error = str(e)
            return render_template('index.html', error=error)
            
if __name__ == "__main__":
    app.run(debug=True)