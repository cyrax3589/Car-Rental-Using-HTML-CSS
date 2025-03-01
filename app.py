from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="car_rental"
)
cursor = conn.cursor(dictionary=True)

# Routes

@app.route('/customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'GET':
        cursor.execute("SELECT * FROM Customers")
        customers = cursor.fetchall()
        return jsonify(customers)
    
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO Customers (first_name, last_name, email, phone, address) VALUES (%s, %s, %s, %s, %s)",
                       (data['first_name'], data['last_name'], data['email'], data['phone'], data['address']))
        conn.commit()
        return jsonify({"message": "Customer added successfully"})

@app.route('/cars', methods=['GET'])
def get_available_cars():
    cursor.execute("SELECT * FROM Cars WHERE status = 'Available'")
    cars = cursor.fetchall()
    return jsonify(cars)

@app.route('/rentals', methods=['POST'])
def rent_car():
    data = request.json
    cursor.execute("INSERT INTO Rentals (customer_id, car_id, start_date, end_date, total_cost, status) VALUES (%s, %s, %s, %s, %s, 'Ongoing')",
                   (data['customer_id'], data['car_id'], data['start_date'], data['end_date'], data['total_cost']))
    conn.commit()
    cursor.execute("UPDATE Cars SET status = 'Rented' WHERE car_id = %s", (data['car_id'],))
    conn.commit()
    return jsonify({"message": "Car rented successfully"})

@app.route('/complete_rental/<int:rental_id>', methods=['PUT'])
def complete_rental(rental_id):
    cursor.execute("UPDATE Rentals SET status = 'Completed' WHERE rental_id = %s", (rental_id,))
    conn.commit()
    return jsonify({"message": "Rental completed"})

@app.route('/')
def serve_frontend():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
