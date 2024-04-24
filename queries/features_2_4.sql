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

--4
-- When viewing a specific apartment unit, the user should be able to view others’ interests so that the 
-- user can join the interest (You are not required to implement the join feature) or post their interest
-- to the unit.

-- View Others Interests 
select i.UnitRentID, i.RoommateCnt, i.MoveInDate, u.first_name, u.last_name  FROM Interests i 
NATURAL JOIN Users u
where i.UnitRentID = 1;

-- post: User types in, goes to python, validates and then posts 
