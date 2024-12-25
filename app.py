import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import pickle
import logging
import warnings
app = Flask(__name__, static_folder='project_folder/static', template_folder='project_folder/templates')

app.secret_key = 'your_secret_key'


warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define the model file path
model_path = os.path.join(os.path.dirname(__file__), 'rf_random.pkl')


# Load the model
try:
    with open(model_path, 'rb') as file:
        model = pickle.load(file)  # Load the serialized model
    logging.info("Model loaded successfully.")
except FileNotFoundError as e:
    logging.error(f"Model file not found: {e}")
    raise
except Exception as e:
    logging.error(f"An error occurred while loading the model: {e}")
    raise




# Route for home page
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("signin"))
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("signin"))
    
    try:
        
        # Extract features from the form using .get() to avoid KeyError
        journey_date = request.form.get("Date_of_Journey")
        dep_time = request.form.get("Dep_Time")
        arrival_time = request.form.get("Arrival_Time")
        duration = request.form.get("Duration")
        airline = request.form.get("Airline")
        source = request.form.get("Source")
        destination = request.form.get("Destination")
        total_stops = request.form.get("Total_Stops")
        
        missing_fields = [field for field in ['Date_of_Journey', 'Dep_Time', 'Arrival_Time', 
                                              'Duration', 'Airline', 'Source', 'Destination', 
                                              'Total_Stops'] if not request.form.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400


        # Convert the Date_of_Journey, Dep_Time, and Arrival_Time to respective parts
        journey_date = pd.to_datetime(journey_date, format='%Y-%m-%d')  
        dep_time = pd.to_datetime(dep_time, format='%H:%M')
        arrival_time = pd.to_datetime(arrival_time, format='%H:%M')

        # Extract the features
        Date_of_Journey_day = journey_date.day
        Date_of_Journey_month = journey_date.month
        Date_of_Journey_year = journey_date.year

        Dep_Time_hour = dep_time.hour
        Dep_Time_minute = dep_time.minute

        Arrival_Time_hour = arrival_time.hour
        Arrival_Time_minute = arrival_time.minute

        # Duration extraction (assuming duration format is 'h m')
        duration_split = duration.split()
        Duration_hour = int(duration_split[0])  # assuming hours
        Duration_minutes = int(duration_split[1])  # assuming minutes
        
        # Total Duration in minutes
        total_duration_minutes = Duration_hour * 60 + Duration_minutes

        # Encoding categorical features
        airline_dict = {'Trujet': 0, 'SpiceJet': 1, 'Air Asia': 2, 'IndiGo': 3, 'GoAir': 4, 'Vistara': 5,
                        'Vistara Premium economy': 6, 'Air India': 7, 'Multiple carriers': 8, 
                        'Multiple carriers Premium economy': 9, 'Jet Airways': 10, 'Jet Airways Business': 11}
        airline_encoded = airline_dict.get(airline, -1)  # Default to -1 if unknown airline

        destination_dict = {'Kolkata': 0, 'Hyderabad': 1, 'Delhi': 2, 'Bangalore': 3, 'Cochin': 4}
        destination_encoded = destination_dict.get(destination, -1)  # Default to -1 if unknown destination

        stops_dict = {'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}
        total_stops_encoded = stops_dict.get(total_stops, -1)  # Default to -1 if unknown stops

        source_dict = {'Banglore': 0, 'Kolkata': 1, 'Delhi': 2, 'Chennai': 3, 'Mumbai': 4}
        source_encoded = source_dict.get(source, -1)  # Default to -1 if unknown source

        # Prepare data for prediction
        data = {
            'Airline': airline_encoded,
            'Destination': destination_encoded,
            'Duration': total_duration_minutes,
            'Total_Stops': total_stops_encoded,
            'Date_of_Journey_day': Date_of_Journey_day,
            'Date_of_Journey_month': Date_of_Journey_month,
            'Dep_Time_hour': Dep_Time_hour,
            'Dep_Time_minute': Dep_Time_minute,
            'Arrival_Time_hour': Arrival_Time_hour,
            'Arrival_Time_minute': Arrival_Time_minute,
            'Duration_hour': Duration_hour,
            'Duration_minutes': Duration_minutes,
            'source_Banglore': 1 if source == 'Banglore' else 0,
            'source_Kolkata': 1 if source == 'Kolkata' else 0,
            'source_Delhi': 1 if source == 'Delhi' else 0,
            'source_Chennai': 1 if source == 'Chennai' else 0,
            'source_Mumbai': 1 if source == 'Mumbai' else 0
        }

        # Convert data to DataFrame
        data_df = pd.DataFrame([data])

        # Predict price using the trained model
        prediction = model.predict(data_df)

        # Render the result page with prediction
        return render_template("result.html", prediction=prediction[0])

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({"error": "Something went wrong"}), 500


# Route for sign-in page
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check user credentials here
        # For demonstration, assume user credentials are valid
        session["user"] = email
        return redirect(url_for("home"))
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")  # Use .get() to avoid KeyError
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Check if all fields are present
        if not name or not email or not password or not confirm_password:
            return "All fields are required", 400
        
        # Check if passwords match
        if password != confirm_password:
            return "Passwords do not match", 400
        
        # Here, you can add logic to save the user to the database
        # Example: save_user_to_database(name, email, password)
        
        # Redirect to login page after successful signup
        return redirect(url_for('signin'))  # Or whatever page you want to redirect to

    return render_template("signup.html")


# Route for logging out
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("signin"))

# Main function to run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
