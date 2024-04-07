1. **Register Pet**
   - **Endpoint:** `/register_pet`
   - **HTTP Method:** POST
   - **Request Body:**
     - `pet_name` (string): The name of the pet
     - `pet_type` (string): The type of the pet
     - `pet_size` (string): The size of the pet
     - `username` (string): The username of the pet's owner
   - **Response:**
     - On success: `{ "flag": 1, "message": "Pet registered successfully" }` (HTTP 200)
     - On failure: `{ "flag": 0, "message": "Failed to register pet" }` (HTTP 400)
     - On error: `{ "flag": 0, "message": "An error occurred while registering the pet" }` (HTTP 500)

2. **Update Pet**
   - **Endpoint:** `/update_pet/<username>/<pet_name>/<pet_type>`
   - **HTTP Method:** PUT
   - **Path Parameters:**
     - `username` (string): The username of the pet's owner
     - `pet_name` (string): The name of the pet
     - `pet_type` (string): The type of the pet
   - **Request Body:**
     - `new_pet_size` (string): The new size of the pet
     - `new_pet_type` (string): The new type of the pet
   - **Response:**
     - On success: `{ "flag": 1, "message": "Pet updated successfully" }` (HTTP 200)
     - On failure: `{ "flag": 0, "message": "Failed to update pet" }` (HTTP 400)
     - On error: `{ "flag": 0, "message": "An error occurred while updating the pet" }` (HTTP 500)

3. **Search Building**
   - **Endpoint:** `/search_building/<building_name>`
   - **HTTP Method:** GET
   - **Path Parameters:**
     - `building_name` (string): The name of the building to search for
   - **Response:**
     - On success: `{ "flag": 1, "data": [...] }` (HTTP 200)
       - The `data` field is an array of objects, where each object represents a row in the result set, with the following keys:
         - `CompanyName`
         - `BuildingName`
         - `AddrNum`
         - `AddrStreet`
         - `AddrCity`
         - `AddrState`
         - `AddrZipCode`
         - `YearBuilt`
         - `NumberOfAvailableUnits`
         - `AmenityType`
         - `AmenityDescription`
     - On failure: `{ "flag": 0, "message": "No building found" }` (HTTP 404)
     - On error: `{ "flag": 0, "message": "An error occurred while searching the building" }` (HTTP 500)

4. **Search Unit**
   - **Endpoint:** `/search_unit/<unit_number>`
   - **HTTP Method:** GET
   - **Path Parameters:**
     - `unit_number` (string): The number of the apartment unit to search for
   - **Response:**
     - On success: `{ "flag": 1, "data": [...] }` (HTTP 200)
       - The `data` field is an array of objects, where each object represents a row in the result set, with the following keys:
         - `CompanyName`
         - `BuildingName`
         - `AddrNum`
         - `AddrStreet`
         - `AddrCity`
         - `AddrState`
         - `AddrZipCode`
         - `YearBuilt`
         - `UnitRentID`
         - `unitNumber`
         - `MonthlyRent`
         - `squareFootage`
         - `AvailableDateForMoveIn`
         - `AmenityType`
         - `AmenityDescription`
     - On failure: `{ "flag": 0, "message": "No unit found with the given number" }` (HTTP 404)
     - On error: `{ "flag": 0, "message": "An error occurred while searching the unit" }` (HTTP 500)

