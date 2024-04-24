-- DDL

-- Insert example users (some with pets, some without)
INSERT INTO Users (username, first_name, last_name, DOB, gender, email, Phone, passwd)
VALUES 
('johndoe', 'John', 'Doe', '1990-05-15', 1, 'johndoe@example.com', '555-1234', 'hashed_password_123'),
('janedoe', 'Jane', 'Doe', '1992-07-20', 2, 'janedoe@example.com', '555-5678', 'hashed_password_456'),
('samgreen', 'Sam', 'Green', '1985-03-30', 1, 'samgreen@example.com', '555-9876', 'hashed_password_789'),
('karengillan', 'Karen', 'Gillan', '1987-11-28', 2, 'kareng@example.com', '555-1212', 'hashed_password_321');

-- Insert pets for users who have them
-- John Doe has two dogs, one medium and one large
-- Jane Doe has one small cat
-- Sam Green has no pets
-- Karen Gillan has one small dog and one medium cat
INSERT INTO Pets (PetName, PetType, PetSize, username)
VALUES 
('Buddy', 'Dog', 'Medium', 'johndoe'),
('Rex', 'Dog', 'Large', 'johndoe'),
('Whiskers', 'Cat', 'Small', 'janedoe'),
('Spot', 'Dog', 'Small', 'karengillan'),
('Mittens', 'Cat', 'Medium', 'karengillan');

-- Insert example apartment buildings
INSERT INTO ApartmentBuilding (CompanyName, BuildingName, AddrNum, AddrStreet, AddrCity, AddrState, AddrZipCode, YearBuilt)
VALUES 
('Sunset Properties', 'Sunset Villas', 100, 'Sunset Blvd', 'Los Angeles', 'CA', '90001', 1990),
('Downtown Living', 'The Metropolitan', 200, 'Main St', 'Los Angeles', 'CA', '90005', 2015);

-- Insert example apartment units
INSERT INTO ApartmentUnit (CompanyName, BuildingName, unitNumber, MonthlyRent, squareFootage, AvailableDateForMoveIn)
VALUES 
('Sunset Properties', 'Sunset Villas', '101', 2500, 850, '2024-06-01'),
('Sunset Properties', 'Sunset Villas', '102', 2700, 900, '2024-07-01'),
('Downtown Living', 'The Metropolitan', '1501', 3200, 1100, '2024-05-15'),
('Downtown Living', 'The Metropolitan', '1502', 3300, 1150, '2024-08-01');

-- Insert pet policies for each building
-- Note: These policies assume all types and sizes of cats and dogs are allowed. Adjust the 'isAllowed' field as necessary.
INSERT INTO PetPolicy (CompanyName, BuildingName, PetType, PetSize, isAllowed, RegistrationFee, MonthlyFee)
VALUES 
('Sunset Properties', 'Sunset Villas', 'Dog', 'Small', TRUE, 200, 30),
('Sunset Properties', 'Sunset Villas', 'Dog', 'Medium', TRUE, 200, 30),
('Sunset Properties', 'Sunset Villas', 'Dog', 'Large', TRUE, 200, 30),
('Sunset Properties', 'Sunset Villas', 'Cat', 'Small', TRUE, 100, 20),
('Sunset Properties', 'Sunset Villas', 'Cat', 'Medium', TRUE, 100, 20),
('Sunset Properties', 'Sunset Villas', 'Cat', 'Large', TRUE, 100, 20),
('Downtown Living', 'The Metropolitan', 'Dog', 'Small', TRUE, 300, 50),
('Downtown Living', 'The Metropolitan', 'Dog', 'Medium', TRUE, 300, 50),
('Downtown Living', 'The Metropolitan', 'Dog', 'Large', TRUE, 300, 50),
('Downtown Living', 'The Metropolitan', 'Cat', 'Small', TRUE, 150, 25),
('Downtown Living', 'The Metropolitan', 'Cat', 'Medium', TRUE, 150, 25),
('Downtown Living', 'The Metropolitan', 'Cat', 'Large', TRUE, 150, 25);



--4 test out 4
-- User 'johndoe' shows interest in unit ID 1, looking for 1 roommate, planning to move in on 2024-06-01
INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
VALUES ('johndoe', 1, 1, '2024-06-01');

-- User 'janedoe' shows interest in unit ID 1, not looking for roommates, planning to move in on 2024-07-01
INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
VALUES ('janedoe', 1, 1, '2024-07-01');

-- User 'samgreen' shows interest in unit ID 2, looking for 2 roommates, planning to move in on 2024-08-01
INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
VALUES ('samgreen', 2, 0, '2024-08-01');

-- User 'karengillan' shows interest in unit ID 3, looking for 1 roommate, planning to move in on 2024-05-15
INSERT INTO Interests (username, UnitRentID, RoommateCnt, MoveInDate)
VALUES ('karengillan', 3, 1, '2024-05-15');
