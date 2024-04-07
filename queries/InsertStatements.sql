-- 2
-- Insert Users with and without pets
INSERT INTO Users (username, first_name, last_name, DOB, gender, email, Phone, passwd) VALUES
('user1', 'John', 'Doe', '1980-01-01', 1, 'john.doe@email.com', '555-0101', 'hashedpasswd1'),
('user2', 'Jane', 'Smith', '1982-02-02', 2, 'jane.smith@email.com', '555-0202', 'hashedpasswd2'),
('user3', 'Alice', 'Johnson', '1984-03-03', 2, 'alice.j@email.com', '555-0303', 'hashedpasswd3');

-- Insert Apartment Buildings
INSERT INTO ApartmentBuilding (CompanyName, BuildingName, AddrNum, AddrStreet, AddrCity, AddrState, AddrZipCode, YearBuilt) VALUES
('CompanyA', 'BuildingA', 123, 'Main St', 'Townsville', 'TS', '12345', 2000),
('CompanyB', 'BuildingB', 456, '2nd St', 'Villagetown', 'VT', '23456', 2010);

-- Insert Apartment Units
INSERT INTO ApartmentUnit (CompanyName, BuildingName, unitNumber, MonthlyRent, squareFootage, AvailableDateForMoveIn) VALUES
('CompanyA', 'BuildingA', '101', 1200, 800, '2024-05-01'),
('CompanyA', 'BuildingA', '102', 1100, 750, '2024-05-15'),
('CompanyB', 'BuildingB', '201', 1300, 850, '2024-06-01');

-- Insert Pet Policies
-- BuildingA allows small dogs but no cats, and BuildingB allows both small dogs and cats
INSERT INTO PetPolicy (CompanyName, BuildingName, PetType, PetSize, isAllowed, RegistrationFee, MonthlyFee) VALUES
('CompanyA', 'BuildingA', 'Dog', 'Small', TRUE, 300, 30),
('CompanyA', 'BuildingA', 'Cat', 'Small', FALSE, NULL, NULL),
('CompanyB', 'BuildingB', 'Dog', 'Small', TRUE, 200, 20),
('CompanyB', 'BuildingB', 'Cat', 'Small', TRUE, 150, 15);

-- Insert Pets for Users
-- User 1 has a small dog, user 2 has a small cat, user 3 has no pets
INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES
('Buddy', 'Dog', 'Small', 'user1'),
('Whiskers', 'Cat', 'Small', 'user2');

INSERT INTO Users (username, first_name, last_name, DOB, gender, email, Phone, passwd) VALUES
('user4', 'Bob', 'Brown', '1986-04-04', 1, 'bob.b@example.com', '555-0404', 'hashedpasswd4');


-- Insert Pets for the new User
-- user4 has a small dog and a small cat
INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES
('Rocky', 'Dog', 'Small', 'user4'),
('Mittens', 'Cat', 'Small', 'user4');









--5 

-- Insert additional Apartment Buildings with the same name 'BuildingX' owned by different companies
INSERT INTO ApartmentBuilding (CompanyName, BuildingName, AddrNum, AddrStreet, AddrCity, AddrState, AddrZipCode, YearBuilt) VALUES
('CompanyC', 'BuildingX', 789, 'Third St', 'Citytown', 'CT', '34567', 2015),
('CompanyD', 'BuildingX', 101, 'Fourth Ave', 'Metropolis', 'MP', '45678', 2020);

-- Insert additional Apartment Units with the same unit number '104' in different buildings and companies
INSERT INTO ApartmentUnit (CompanyName, BuildingName, unitNumber, MonthlyRent, squareFootage, AvailableDateForMoveIn) VALUES
('CompanyA', 'BuildingA', '104', 1400, 900, '2024-07-01'),
('CompanyB', 'BuildingB', '104', 1450, 850, '2024-07-15'),
('CompanyC', 'BuildingX', '104', 1500, 950, '2024-08-01'),
('CompanyD', 'BuildingX', '104', 1550, 1000, '2024-08-15');

-- Insert Amenities for 'BuildingX' under both companies
INSERT INTO Amenities (aType, Description) VALUES
('Pool', 'Swimming Pool'),
('Gym', 'Fitness Center');

-- Assume 'Provides' entries for 'BuildingX' have been made
INSERT INTO Provides (aType, CompanyName, BuildingName, Fee, waitingList) VALUES
('Pool', 'CompanyC', 'BuildingX', 0, 0),
('Gym', 'CompanyC', 'BuildingX', 0, 0),
('Pool', 'CompanyD', 'BuildingX', 0, 0),
('Gym', 'CompanyD', 'BuildingX', 0, 0);