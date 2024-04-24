-- Queries
--2 
-- Given the exact building name and company name, the application should return a list of units for rent and 
-- their basic information (monthly rent, square footage, available date for move-in, xbxb etc.)
-- b. Based on the registered information of the pet of user, the system shows whether whether the pet is allowed.
SELECT 
    DISTINCT(au.UnitRentID), 
    au.unitNumber, 
    au.MonthlyRent, 
    au.squareFootage, 
    au.AvailableDateForMoveIn
FROM 
    ApartmentUnit au
    INNER JOIN PetPolicy pp ON au.CompanyName = pp.CompanyName AND au.BuildingName = pp.BuildingName
    LEFT JOIN Pets p ON pp.PetType = p.PetType AND pp.PetSize = p.PetSize AND p.username = 'johndoe'
WHERE 
    -- Filtering by the building name and company name (e.g., 'Sunset Villas' of 'Sunset Properties')
    au.BuildingName = 'Sunset Villas' AND
    au.CompanyName = 'Sunset Properties' AND
    -- Ensure that all pet policies are met for the user's pets
    (pp.isAllowed = TRUE OR p.PetName IS NULL)
GROUP BY 
    au.UnitRentID, 
    au.unitNumber, 
    au.MonthlyRent, 
    au.squareFootage, 
    au.AvailableDateForMoveIn
HAVING 
    COUNT(DISTINCT p.PetType, p.PetSize) = (SELECT COUNT(DISTINCT up.PetType, up.PetSize) FROM Pets up WHERE username = 'johndoe')
    OR NOT EXISTS (SELECT 1 FROM Pets WHERE username = 'johndoe');


-- creating a view for later queries
CREATE VIEW AuExtra as
SELECT au.*, CONCAT(
	(SELECT COUNT(*) 
     FROM Rooms r 
     WHERE au.UnitRentID = r.UnitRentID and r.name like 'bedroom%'),'b',
     (SELECT COUNT(*) 
     FROM Rooms r 
     WHERE au.UnitRentID = r.UnitRentID and r.name like 'bathroom%'),'b') as XbXb
FROM ApartmentUnit au;



-- NEW 2 
SELECT 
    DISTINCT(au.UnitRentID), 
    au.unitNumber, 
    au.MonthlyRent, 
    au.squareFootage, 
    au.AvailableDateForMoveIn,
    au.xbxb
FROM 
    AuExtra au
    INNER JOIN PetPolicy pp ON au.CompanyName = pp.CompanyName AND au.BuildingName = pp.BuildingName
    LEFT JOIN Pets p ON pp.PetType = p.PetType AND pp.PetSize = p.PetSize AND p.username = 'lh3388'
WHERE 
    -- Filtering by the building name and company name (e.g., 'Sunset Villas' of 'Sunset Properties')
    au.BuildingName = 'Mary Island' AND
    au.CompanyName = 'Ramos Inc' AND
    -- Ensure that all pet policies are met for the user's pets
    (pp.isAllowed = TRUE OR p.PetName IS NULL)
GROUP BY 
    au.UnitRentID, 
    au.unitNumber, 
    au.MonthlyRent, 
    au.squareFootage, 
    au.AvailableDateForMoveIn
HAVING 
    COUNT(DISTINCT p.PetType, p.PetSize) = (SELECT COUNT(DISTINCT up.PetType, up.PetSize) FROM Pets up WHERE username = 'lh3388')
    OR NOT EXISTS (SELECT 1 FROM Pets WHERE username = 'lh3388');

--4
-- When viewing a specific apartment unit, the user should be able to view others’ interests so that the 
-- user can join the interest (You are not required to implement the join feature) or post their interest
-- to the unit.

-- View Others Interests 
select i.UnitRentID, i.RoommateCnt, i.MoveInDate, u.first_name, u.last_name  FROM Interests i 
NATURAL JOIN Users u
where i.UnitRentID = 1;

-- post: User types in, goes to python, validates and then posts 





--8
SELECT i.UnitRentID, i.RoommateCnt, i.MoveInDate, u.first_name, u.last_name, u.gender, u.Phone, u.email
FROM Interests i
NATURAL JOIN Users u
WHERE i.MoveInDate > '2024-05-28' AND i.UnitRentID = 18 and i.RoommateCnt>=0;

--9
SELECT au.XbXb, AVG(au.MonthlyRent) AS AverageMonthlyRent
FROM AuExtra au 
NATURAL JOIN ApartmentBuilding ab
WHERE ab.AddrZipCode = 30113
GROUP BY au.XbXb;

--10 
--Create a table called favorite 
CREATE TABLE Favorite (
    UnitRentID INT,
    username VARCHAR(20),
    PRIMARY KEY (UnitRentID, username),
    FOREIGN KEY (UnitRentID) REFERENCES ApartmentUnit (UnitRentID),
    FOREIGN KEY (username) REFERENCES Users (username)
);

--add to favorite
INSERT INTO Favorite (UnitRentID, username) VALUES
(1, 'aj25082');

--view all favorited apartments
SELECT au.UnitRentID, au.MonthlyRent, au.squareFootage, au.XbXb, ab.CompanyName, ab.BuildingName, ab.AddrZipCode, p.aType
FROM Favorite f 
NATURAL JOIN auextra au 
NATURAL JOIN ApartmentBuilding ab
INNER JOIN Provides p on p.CompanyName = ab.CompanyName and p.BuildingName = ab.BuildingName
WHERE f.username = 'aj25082';

-- TODO: Extra feature: View Others' interests on the apartment

--11
SELECT au.UnitRentID, au.MonthlyRent, (
    SELECT AVG(au2.MonthlyRent)
    FROM auextra au2
    NATURAL JOIN ApartmentBuilding ab2
    WHERE ABS(au.squareFootage - au2.squareFootage) <= 0.10 * au.squareFootage
	AND ab2.AddrCity = ab.AddrCity AND au2.UnitRentID != au.UnitRentID) AS Extra_View
FROM
auextra au 
NATURAL JOIN ApartmentBuilding ab
WHERE au.UnitRentID = 3;

