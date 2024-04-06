Users
-----
username (PK)
first_name
last_name
DOB
gender
email
Phone
passwd

Pets
----
PetName (PK)
PetType (PK)
PetSize
username (FK -> Users.username)

ApartmentBuilding
-----------------
CompanyName (PK)
BuildingName (PK)
AddrNum
AddrStreet
AddrCity
AddrState
AddrZipCode
YearBuilt

ApartmentUnit
-------------
UnitRentID (PK, Auto-Increment)
CompanyName (FK -> ApartmentBuilding.CompanyName)
BuildingName (FK -> ApartmentBuilding.BuildingName)
unitNumber
MonthlyRent
squareFootage
AvailableDateForMoveIn

Rooms
-----
name (PK)
squareFootage
description
UnitRentID (FK -> ApartmentUnit.UnitRentID)

PetPolicy
---------
CompanyName (PK, FK -> ApartmentBuilding.CompanyName)
BuildingName (PK, FK -> ApartmentBuilding.BuildingName)
PetType (PK)
PetSize (PK)
isAllowed
RegistrationFee
MonthlyFee

Amenities
---------
aType (PK)
Description

Interests
---------
username (PK, FK -> Users.username)
UnitRentID (PK, FK -> ApartmentUnit.UnitRentID)
RoommateCnt
MoveInDate

AmenitiesIn
-----------
aType (PK, FK -> Amenities.aType)
UnitRentID (PK, FK -> ApartmentUnit.UnitRentID)

Provides
--------
aType (PK, FK -> Amenities.aType)
CompanyName (PK, FK -> ApartmentBuilding.CompanyName)
BuildingName (PK, FK -> ApartmentBuilding.BuildingName)
Fee
waitingList
