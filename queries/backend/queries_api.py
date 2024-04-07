import flask 
from flask import Flask , render_template, session, request, redirect, url_for, jsonify
import psycopg2, hashlib, os
from flask_cors import CORS
import json

app = Flask(__name__) 
app.secret_key = os.urandom(24)
CORS(app)

'''
Feature 2. Register and Update Pet

I've kept a put and a post for editing pet info, check which works and go about it
'''
@app.route('/register_pet', methods=['POST'])
def register_pet():
    data_dict = {}
    for key, value in request.form.items():
        data_dict = json.loads(key)

    try:
        pet_name = data_dict['pet_name']
        pet_type = data_dict['pet_type']
        pet_size = data_dict['pet_size']
        username = data_dict['username']

        query = "INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES (%s, %s, %s, %s);"
        parameters = (pet_name, pet_type, pet_size, username)

        result = executeQueryResult(query, parameters)

        if result:
            return jsonify({'flag': 1, 'message': 'Pet registered successfully'}), 200
        else:
            return jsonify({'flag': 0, 'message': 'Failed to register pet'}), 400
    except Exception as e:
        print(f"Error registering pet: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while registering the pet'}), 500


@app.route('/update_pet', methods=['POST'])
def update_pet():
    try:
        username = request.form['username']
        pet_name = request.form['pet_name']
        pet_type = request.form['pet_type']
        new_pet_size = request.form['new_pet_size']
        new_pet_type = request.form['new_pet_type']

        query = "UPDATE Pets SET PetSize = %s, PetType = %s WHERE username = %s AND PetName = %s AND PetType = %s;"
        parameters = (new_pet_size, new_pet_type, username, pet_name, pet_type)

        result = executeQueryResult(query, parameters)

        if result:
            return jsonify({'flag': 1, 'message': 'Pet updated successfully'}), 200
        else:
            return jsonify({'flag': 0, 'message': 'Failed to update pet'}), 400
    except Exception as e:
        print(f"Error updating pet: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while updating the pet'}), 500



# @app.route('/update_pet/<username>/<pet_name>/<pet_type>', methods=['PUT'])
# def update_pet(username, pet_name, pet_type):
#     try:
#         new_pet_size = request.form['new_pet_size']
#         new_pet_type = request.form['new_pet_type']

#         query = "UPDATE Pets SET PetSize = %s, PetType = %s WHERE username = %s AND PetName = %s AND PetType = %s;"
#         parameters = (new_pet_size, new_pet_type, username, pet_name, pet_type)

#         result = executeQueryResult(query, parameters)

#         if result:
#             return jsonify({'flag': 1, 'message': 'Pet updated successfully'}), 200
#         else:
#             return jsonify({'flag': 0, 'message': 'Failed to update pet'}), 400
#     except Exception as e:
#         print(f"Error updating pet: {e}")
#         return jsonify({'flag': 0, 'message': 'An error occurred while updating the pet'}), 500



''' 
5. Search by building 
Search by Unit
'''
@app.route('/search_building/<building_name>', methods=['GET'])
def search_building(building_name):
    try:
        query = """
            SELECT AB.CompanyName, AB.BuildingName, AB.AddrNum, AB.AddrStreet, AB.AddrCity, AB.AddrState, AB.AddrZipCode, AB.YearBuilt, 
                   AvailableUnits.NumberOfAvailableUnits, A.aType AS AmenityType, A.Description AS AmenityDescription
            FROM ApartmentBuilding AB
            LEFT JOIN (
                SELECT CompanyName, BuildingName, COUNT(*) AS NumberOfAvailableUnits
                FROM ApartmentUnit
                WHERE AvailableDateForMoveIn > CURRENT_DATE
                GROUP BY CompanyName, BuildingName
            ) AS AvailableUnits ON AB.CompanyName = AvailableUnits.CompanyName AND AB.BuildingName = AvailableUnits.BuildingName
            LEFT JOIN Provides P ON AB.CompanyName = P.CompanyName AND AB.BuildingName = P.BuildingName
            LEFT JOIN Amenities A ON P.aType = A.aType
            WHERE AB.BuildingName = %s
            ORDER BY AB.CompanyName, AB.BuildingName, A.aType;
        """
        parameters = (building_name,)

        result = fetchQueryResult(query, parameters)

        if result:
            data = []
            for row in result:
                data.append({
                    'CompanyName': row[0],
                    'BuildingName': row[1],
                    'AddrNum': row[2],
                    'AddrStreet': row[3],
                    'AddrCity': row[4],
                    'AddrState': row[5],
                    'AddrZipCode': row[6],
                    'YearBuilt': row[7],
                    'NumberOfAvailableUnits': row[8],
                    'AmenityType': row[9],
                    'AmenityDescription': row[10]
                })
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No building found'}), 404
    except Exception as e:
        print(f"Error searching building: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while searching the building'}), 500


@app.route('/search_unit/<unit_number>', methods=['GET'])
def search_unit(unit_number):
    try:
        query = """
            SELECT AB.CompanyName, AB.BuildingName, AB.AddrNum, AB.AddrStreet, AB.AddrCity, AB.AddrState, AB.AddrZipCode, AB.YearBuilt,
                   AU.UnitRentID, AU.unitNumber, AU.MonthlyRent, AU.squareFootage, AU.AvailableDateForMoveIn,
                   PA.aType AS AmenityType, A.Description AS AmenityDescription
            FROM ApartmentUnit AU
            INNER JOIN ApartmentBuilding AB ON AU.CompanyName = AB.CompanyName AND AU.BuildingName = AB.BuildingName
            LEFT JOIN Provides PA ON AB.CompanyName = PA.CompanyName AND AB.BuildingName = PA.BuildingName
            LEFT JOIN Amenities A ON PA.aType = A.aType
            WHERE AU.unitNumber = %s;
        """
        parameters = (unit_number,)

        result = fetchQueryResult(query, parameters)

        if result:
            data = []
            for row in result:
                data.append({
                    'CompanyName': row[0],
                    'BuildingName': row[1],
                    'AddrNum': row[2],
                    'AddrStreet': row[3],
                    'AddrCity': row[4],
                    'AddrState': row[5],
                    'AddrZipCode': row[6],
                    'YearBuilt': row[7],
                    'UnitRentID': row[8],
                    'unitNumber': row[9],
                    'MonthlyRent': row[10],
                    'squareFootage': row[11],
                    'AvailableDateForMoveIn': row[12],
                    'AmenityType': row[13],
                    'AmenityDescription': row[14]
                })
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No unit found with the given number'}), 404
    except Exception as e:
        print(f"Error searching unit: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while searching the unit'}), 500



def fetchQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    result = cur_object.fetchall()

    return result

def executeQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )

    cur_object = con.cursor()

    cur_object.execute(query, parameters)

    con.commit()

    return True

@app.route('/trial')
def trialAPI():
    return jsonify(fetchQueryResult("Select * from Users", {}))


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=8989)


''' 
import requests
url = "http://localhost:8989/register_pet"  # Update the port if your app runs on a different one
data = {
    'pet_name': 'Buddy',
    'pet_type': 'Dog',
    'pet_size': 'Medium',
    'username': 'user1'
}

response = requests.post(url, data=data)
print(response.json())


url = "http://localhost:8989/update_pet"
data = {
    'username': 'user1',
    'pet_name': 'Buddy',
    'pet_type': 'Dog',
    'new_pet_size': 'Small',  # Assuming you're changing the size
    'new_pet_type': 'Dog'  # Assuming the type remains the same, but it could be changed as well
}

response = requests.post(url, data=data)
print(response.json())



url = "http://localhost:8989/search_building/BuildingX"
response = requests.get(url)
print(response.json())


url = "http://localhost:8989/search_unit/104"
response = requests.get(url
print(response.json())
'''