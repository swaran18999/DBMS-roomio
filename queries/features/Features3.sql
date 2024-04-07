--3.
-- Register Pet
INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES ('NewPetName', 'NewPetType', 'NewPetSize', 'UsernameOfOwner');

--Edit Pet
UPDATE Pets
SET PetSize = 'UpdatedSize', PetType = 'UpdatedType'
WHERE username = 'UsernameOfOwner' AND PetName = 'ExistingPetName' AND PetType = 'ExistingPetType';


--Postgres
INSERT INTO Pets (PetName, PetType, PetSize, username) VALUES ('Fluffy', 'Cat', 'Small', 'user2');

-- Update an existing pet
UPDATE Pets SET PetSize = 'Medium', PetType = 'Persian' 
WHERE username = 'user2' AND PetName = 'Whiskers' AND PetType = 'Cat';