import flask 
from flask import Flask , render_template, request, redirect, url_for, jsonify
import psycopg2, hashlib, os
from flask_cors import CORS
import json
from urllib.parse import unquote
from functools import wraps

session = {}

app = Flask(__name__) 
app.secret_key = os.urandom(24)
CORS(app)

def getEncryptedPassword(password):
    salt = "random_salt"
    hash_password = hashlib.sha256((password + salt).encode()).hexdigest()
    return hash_password

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['username'] == None:
            return jsonify({'flag': 2, 'message': 'User not authenticated'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    print("/ called", session.get('loggedIn'))
    try:
        if(session.get('loggedIn')):
            return {'flag': 1, 'message': 'User is logged in'}
        else: 
            return {'flag': 2, 'message': 'User is not logged in'}
    except Exception as e:
        return {'flag': 0, 'message': e}


@app.route('/signup' , methods = ['POST'])
def signup():
    data_dict = request.get_json()
    
    userName = data_dict['newUsername']
    password = data_dict['newPassword']
    dob = data_dict['newDOB']
    email = data_dict['newEmail']
    firstName = data_dict['newFirstName']
    lastName = data_dict['newLastName']
    phone = data_dict['newPhone']
    gender = data_dict['newGender']

    enc_password = getEncryptedPassword(password)
    
    query = "INSERT INTO Users (username, first_name, last_name, DOB, gender, email, Phone, passwd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"

    parameters = (userName, firstName, lastName, dob, gender, email, phone, enc_password)

    result = executeQueryResult(query, parameters)

    if result == True:
        print('Register Successful !')
        return jsonify({
            'flag': 1,
            'message': 'Signup successfull'
        })
    else:
        print("Registration Unsuccessful !")
        return jsonify({'flag' : 0})

@app.route('/login' , methods = ['POST'])
def login():
    data_dict = request.get_json()
    username = data_dict['username']
    password = data_dict['password']   

    enc_password = getEncryptedPassword(password)

    query = "SELECT username, email FROM Users WHERE username = %s and passwd = %s;"

    parameters = (username, enc_password)

    result = fetchQueryResult(query, parameters)

    if not result == []:
        session['username'] = result[0][0]
        session['email'] = result[0][1]
        session['loggedIn'] = True

        return jsonify({
            'flag': 1,
            'message': "Successfully logged in"
        })

    else: 
        return jsonify({'flag' : 0})

@app.route('/logout', methods = ['POST'])
def logout():
    session['username'] = None
    session['email'] = None
    session['loggedIn'] = False

    return jsonify({'flag' : 1, 'message': "Successfully logged out"})


'''
Feature 2. Register and Update Pet

I've kept a put and a post for editing pet info, check which works and go about it
'''
@app.route('/get_pet')
@login_required
def get_pet():
    try:
        username = session['username']  # Get the username from the JSON data

        query = "SELECT * FROM Pets AS p WHERE username = %s ORDER BY p.petname;"
        parameters = (username,)

        pets = fetchQueryResult(query, parameters)
        print(pets)

        if pets:
            pet_list = [{'pet_name': pet[0], 'pet_type': pet[1], 'pet_size': pet[2]} for pet in pets]
            return jsonify({'flag': 1, 'pets': pet_list}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No pets found for the given username'}), 404
    except Exception as e:
        print(f"Error getting pets: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred while getting pets {e}'}), 500


@app.route('/register_pet', methods=['POST'])
@login_required
def register_pet():
    data_dict = request.get_json()

    try:
        pet_name = data_dict['pet_name']
        pet_type = data_dict['pet_type']
        pet_size = data_dict['pet_size']
        username = session['username']

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
@login_required
def update_pet():
    data_dict = request.get_json()

    try:
        username = session['username']
        pet_name = data_dict['old_pet_name']
        pet_type = data_dict['old_pet_type']
        new_pet_size = data_dict['pet_size']
        new_pet_type = data_dict['pet_type']

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

@app.route('/delete_pet', methods=['POST'])
@login_required
def delete_pet():
    try:
        username = session['username']
        data_dict = request.get_json()

        pet_name = data_dict.get('pet_name')
        pet_type = data_dict.get('pet_type')

        if not pet_name or not pet_type:
            return jsonify({'flag': 0, 'message': 'Pet name and type are required'}), 400

        query = "DELETE FROM Pets WHERE username = %s AND PetName = %s AND PetType = %s;"
        parameters = (username, pet_name, pet_type)

        result = executeQueryResult(query, parameters)

        if result:
            return jsonify({'flag': 1, 'message': 'Pet deleted successfully'}), 200
        else:
            return jsonify({'flag': 0, 'message': 'Failed to delete pet'}), 400
    except Exception as e:
        print(f"Error deleting pet: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while deleting the pet'}), 500

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

@app.route('/search_apartment', methods=['POST'])
def search_apartment():
    try:
        data_dict = request.get_json()
        company_name = data_dict.get('companyName')
        building_name = data_dict.get('buildingName')
        
        if not company_name or not building_name:
            return jsonify({'flag': 0, 'message': 'Company name and building name are required'}), 400

        query = """
            SELECT UnitRentID, CompanyName, BuildingName, UnitNumber, MonthlyRent, SquareFootage, AvailableDateForMoveIn
            FROM ApartmentUnit
            WHERE CompanyName = %s AND BuildingName = %s;
        """
        parameters = (company_name, building_name)

        result = fetchQueryResult(query, parameters)

        if result:
            data = []
            for row in result:
                data.append({
                    'UnitRentID': row[0],
                    'CompanyName': row[1],
                    'BuildingName': row[2],
                    'UnitNumber': row[3],
                    'MonthlyRent': row[4],
                    'SquareFootage': row[5],
                    'AvailableDateForMoveIn': row[6].isoformat()  # Convert date to ISO format
                })
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'data': [], 'message': 'No apartments found for the given company and building'}), 200
    except Exception as e:
        print(f"Error searching apartments: {e}")
        return jsonify({'flag': 0, 'message': 'An error occurred while searching apartments'}), 500

''' 
5. Search by building 
Search by Unit
Creating useful views 

CREATE VIEW AuExtra as
SELECT au.*, CONCAT(
	(SELECT COUNT(*) 
     FROM Rooms r 
     WHERE au.UnitRentID = r.UnitRentID and r.name like 'bedroom%'),'b',
     (SELECT COUNT(*) 
     FROM Rooms r 
     WHERE au.UnitRentID = r.UnitRentID and r.name like 'bathroom%'),'b') as XbXb
FROM ApartmentUnit au;



create view ab_formatted as
SELECT 
    companyname, 
    buildingname, 
    CONCAT_WS(', ', addrnum, addrstreet, addrcity, addrstate, addrzipcode) as Address, 
    yearbuilt 
FROM 
    apartmentbuilding;

create view amenitiesoffered as 
select companyname, buildingname, string_agg(atype,', ') as amenitieslist
from Provides
group by companyname, buildingname;

'''

@app.route('/search_building', methods=['GET'])
def search_building():
    building_name = request.args.get('buildingName')
    if not building_name:
        return jsonify({'flag': 0, 'message': 'Building name parameter is required'}), 400

    try:
        query = """
        select * from amenitiesoffered ao
        natural join
        (select ab.companyname, ab.buildingname, ab.address, ab.yearbuilt,COUNT(au.unitrentid) as Numunitsavailableforrent
        from ab_formatted ab
        natural join auextra au
        group by ab.companyname, ab.buildingname, ab.address, ab.yearbuilt) as buildings
        where buildingname = %s;
        """
        parameters = (building_name,)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'CompanyName': row[0],
                'BuildingName': row[1],
                'amenitieslist': row[2],
                'Address': row[3],
                'YearBuilt': row[4],
                'NumUnitsAvailableForRent': row[5]
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'data': [], 'message': 'No buildings found with the specified name'}), 200
    except Exception as e:
        print(f"Error searching by building: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500


@app.route('/search_unit/<unit_number>', methods=['GET'])
def search_unit(unit_number):
    # {"unitRentID":1}
    print(request.args)
    unit_rent_id = unit_number
    print('here',unit_rent_id)
    if not unit_rent_id:
        return jsonify({'flag': 0, 'message': 'Unit Rent ID parameter is required'}), 400

    try:
        query = """
        SELECT au.UnitRentID, ab.companyname, ab.buildingname, au.unitNumber, au.MonthlyRent, au.squareFootage, au.AvailableDateForMoveIn, ao.amenitieslist
        FROM auextra au
        NATURAL JOIN ab_formatted ab
        NATURAL JOIN amenitiesoffered ao
        WHERE au.unitrentid = %s;
        """
        parameters = (unit_rent_id,)
        result = fetchQueryResult(query, parameters)

        if result:
            for row in result:
                data = {
                    'UnitRentID': row[0],#
                    'CompanyName': row[1],#
                    'BuildingName': row[2],#
                    'UnitNumber': row[3],#
                    'MonthlyRent': row[4],#
                    'SquareFootage': row[5],#
                    'AvailableDateForMoveIn': row[6].isoformat(),#
                    'AmenitiesList': row[7]  # 
                } 
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'data': [], 'message': 'No unit found with the specified ID'}), 200
    except Exception as e:
        print(f"Error searching by unit: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500


# 2
@app.route('/check_pet_policy_compatibility', methods=['GET'])
@login_required
def get_pet_policies():
    username = session['username']
    company_name = request.args.get('company_name')
    building_name = request.args.get('building_name')

    # Validate required parameters
    if not all([username, company_name, building_name]):
        return jsonify({'flag': 0, 'message': 'Missing required query parameters'}), 400

    try:
        query = """
        SELECT 
            pp.companyname,
            pp.buildingname,
            p.PetType,
            p.PetSize,
            pp.isAllowed,
            CASE 
                WHEN pp.isAllowed THEN 'Allowed'
                ELSE 'Not Allowed' 
            END AS PetStatus,
            pp.RegistrationFee,
            pp.MonthlyFee
        FROM 
            Pets p
        JOIN 
            Users u ON p.username = u.username
        JOIN 
            PetPolicy pp ON pp.PetType = p.PetType AND pp.PetSize = p.PetSize
        WHERE 
            u.username = %s AND 
            pp.CompanyName = %s AND 
            pp.BuildingName = %s;
        """
        parameters = (username, company_name, building_name)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'CompanyName': row[0],
                'BuildingName': row[1],
                'PetType': row[2],
                'PetSize': row[3],
                'IsAllowed': row[4],
                'PetStatus': row[5],
                'RegistrationFee': row[6],
                'MonthlyFee': row[7]
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No pet policies found for the specified parameters'}), 404
    except Exception as e:
        print(f"Error in fetching pet policies: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

''' 
4.
When viewing a specific apartment unit, the user should be able to view others' interests so that the user can join 
the interest (You are not required to implement the join feature) or post their interest to the unit.
'''

@app.route('/add_interest', methods=['POST'])
@login_required
def add_interest():
    data = request.get_json()

    if not data or 'UnitRentID' not in data or 'RoommateCnt' not in data or 'MoveInDate' not in data:
        return jsonify({'flag': 0, 'message': 'Missing required parameters'}), 400
    
    username = session['username']
    unit_rent_id = data['UnitRentID']
    roommate_cnt = data['RoommateCnt']
    move_in_date = data['MoveInDate']

    try:
        query = """
        INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
        VALUES (%s, %s, %s, %s);
        """
        parameters = (username, unit_rent_id, roommate_cnt, move_in_date)
        executeQueryResult(query, parameters) 

        return jsonify({'flag': 1, 'message': 'Interest added successfully'}), 201
    except Exception as e:
        print(f"Error adding interest: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

@app.route('/view_interests/<unit_number>', methods=['GET'])
@login_required
def view_interests(unit_number):
    # {"UnitRentID":5}
    # unit_rent_id = request.args.get('UnitRentID')
    if not unit_number:
        return jsonify({'flag': 0, 'message': 'UnitRentID parameter is required'}), 400

    try:
        query = """
        SELECT i.UnitRentID, i.RoommateCnt, i.MoveInDate, u.first_name, u.last_name, u.username
        FROM Interests i 
        NATURAL JOIN Users u
        WHERE i.UnitRentID = %s;
        """
        parameters = (unit_number)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'UnitRentID': row[0],
                'RoommateCnt': row[1],
                'MoveInDate': row[2].isoformat(),
                'FirstName': row[3],
                'LastName': row[4],
                'isUser': row[5] == session['username']
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No interests found for the specified UnitRentID'}), 404
    except Exception as e:
        print(f"Error in fetching interests: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

@app.route('/delete_interest', methods=['POST'])
@login_required
def delete_interest():
    data = request.get_json()
    if not data or 'UnitRentID' not in data or 'RoommateCnt' not in data or 'MoveInDate' not in data:
        return jsonify({'flag': 0, 'message': 'Missing required parameters'}), 400
    
    username = session['username']
    unit_rent_id = data['UnitRentID']
    roommate_cnt = data['RoommateCnt']
    move_in_date = data['MoveInDate']

    try:
        query = "DELETE FROM Interests WHERE username = %s AND UnitRentID = %s AND RoommateCnt = %s AND MoveInDate = %s;"
        parameters = (username, unit_rent_id, roommate_cnt, move_in_date)
        executeQueryResult(query, parameters)

        return jsonify({'flag': 1, 'message': 'Interest added successfully'}), 201
    except Exception as e:
        print(f"Error adding interest: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

# 8
@app.route('/search_interests', methods=['GET'])
def search_interests():
    # Retrieve query parameters
    move_in_date = request.args.get('MoveInDate')
    unit_rent_id = request.args.get('UnitRentID')
    roommate_cnt = request.args.get('RoommateCnt')

    # Validate required parameters
    if not all([move_in_date, unit_rent_id, roommate_cnt]):
        return jsonify({'flag': 0, 'message': 'Missing required query parameters'}), 400

    try:
        query = """
        SELECT i.UnitRentID, i.RoommateCnt, i.MoveInDate, u.first_name, u.last_name, u.gender, u.Phone, u.email
        FROM Interests i
        NATURAL JOIN Users u
        WHERE i.MoveInDate = %s AND i.UnitRentID = %s AND i.RoommateCnt = %s;
        """
        parameters = (move_in_date, unit_rent_id, roommate_cnt)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'UnitRentID': row[0],
                'RoommateCount': row[1],
                'MoveInDate': row[2],
                'FirstName': row[3],
                'LastName': row[4],
                'Gender': row[5],
                'Phone': row[6],
                'Email': row[7]
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No interests found matching criteria'}), 404
    except Exception as e:
        print(f"Error in fetching interests: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

# 9
@app.route('/average_rent_by_zipcode', methods=['GET'])
def average_rent_by_xbxb():
    # Retrieve the zip code from query parameters
    zip_code = request.args.get('zip_code')
    if not zip_code:
        return jsonify({'flag': 0, 'message': 'Zip code parameter is required'}), 400

    try:
        query = """
        SELECT au.XbXb, AVG(au.MonthlyRent) AS AverageMonthlyRent
        FROM AuExtra au 
        NATURAL JOIN ApartmentBuilding ab
        WHERE ab.AddrZipCode = %s
        GROUP BY au.XbXb;
        """
        parameters = (zip_code,)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{'XbXb': row[0], 'AverageMonthlyRent': float(row[1])} for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No data found for the specified zip code'}), 404
    except Exception as e:
        print(f"Error in fetching average rent by XbXb: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

# 11
@app.route('/rent_extra_view', methods=['GET'])
def rent_extra_view():
    # Retrieve the UnitRentID from query parameters
    print(request.args)
    unit_rent_id = request.args.get('UnitRentID')
    if not unit_rent_id:
        return jsonify({'flag': 0, 'message': 'UnitRentID parameter is required'}), 400

    try:
        query = """
        SELECT au.UnitRentID, au.MonthlyRent, (
            SELECT AVG(au2.MonthlyRent)
            FROM auextra au2
            NATURAL JOIN ApartmentBuilding ab2
            WHERE ABS(au.squareFootage - au2.squareFootage) <= 0.10 * au.squareFootage
            AND ab2.AddrCity = ab.AddrCity AND au2.UnitRentID != au.UnitRentID) AS Extra_View
        FROM
        auextra au 
        NATURAL JOIN ApartmentBuilding ab
        WHERE au.UnitRentID = %s;
        """
        parameters = (unit_rent_id,)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'UnitRentID': row[0],
                'MonthlyRent': float(row[1]),
                'ExtraView': float(row[2]) if row[2] is not None else None
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            print("Result was empty")
            return jsonify({'flag': 0, 'message': 'No data found for the specified UnitRentID'}), 404
    except Exception as e:
        print(f"Error in fetching rent extra view: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500



def fetchQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )
    try:
        cur_object = con.cursor()

        cur_object.execute(query, parameters)

        result = cur_object.fetchall()
    except Exception as e:
        print(f"Error occured while processing query {query} \n Error: {e}")
        result = None
    return result

def executeQueryResult(query, parameters):
    con = psycopg2.connect(
        database="klzhcbxk",
        user="klzhcbxk",
        password="1HbbkUWWZxRHNJR_AkxBUg1Dk_8OMcjx",
        host="batyr.db.elephantsql.com",
        port= '5432'
    )
    try:
        cur_object = con.cursor()

        cur_object.execute(query, parameters)

        con.commit()

        return True
    except Exception as e:
        print("Post failed due to",e)
        return False

# 13 Comment system
@app.route('/add_comment', methods=['POST'])
@login_required
def add_comment():
    data = request.get_json()

    if not data or 'UnitRentID' not in data or 'Rating' not in data or 'Comment' not in data:
        return jsonify({'flag': 0, 'message': 'Missing required parameters'}), 400
    
    username = session['username']
    unit_rent_id = data['UnitRentID']
    rating = data['Rating']
    comment_text = data['Comment']

    try:
        query = """
        INSERT INTO Comments (username, UnitRentID, Rating, Comment)
        VALUES (%s, %s, %s, %s);
        """
        parameters = (username, unit_rent_id, rating, comment_text)
        executeQueryResult(query, parameters) 

        return jsonify({'flag': 1, 'message': 'Comment added successfully'}), 201
    except Exception as e:
        print(f"Error adding comment: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

@app.route('/view_comments/<unit_number>', methods=['GET'])
@login_required
def view_comments(unit_number):
    if not unit_number:
        return jsonify({'flag': 0, 'message': 'UnitRentID parameter is required'}), 400

    try:
        query = """
        SELECT c.UnitRentID, c.Rating, c.Comment, u.first_name, u.last_name, u.username, c.CommentID
        FROM Comments c 
        NATURAL JOIN Users u
        WHERE c.UnitRentID = %s;
        """
        parameters = (unit_number,)
        result = fetchQueryResult(query, parameters)

        if result:
            data = [{
                'UnitRentID': row[0],
                'Rating': row[1],
                'Comment': row[2],
                'FirstName': row[3],
                'LastName': row[4],
                'UserName': row[5],
                'CommentID': row[6],
                'isUser': row[5] == session['username']
            } for row in result]
            return jsonify({'flag': 1, 'data': data}), 200
        else:
            return jsonify({'flag': 0, 'message': 'No comments found for the specified UnitRentID'}), 404
    except Exception as e:
        print(f"Error in fetching comments: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500

@app.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    data = request.get_json()
    
    username = session['username']
    CommentID = data['CommentID']

    try:
        query = "DELETE FROM Comments WHERE username = %s AND CommentID = %s;"
        parameters = (username, CommentID)
        executeQueryResult(query, parameters)

        return jsonify({'flag': 1, 'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return jsonify({'flag': 0, 'message': f'An error occurred: {e}'}), 500


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