-- search by building
SELECT
    AB.CompanyName,
    AB.BuildingName,
    AB.AddrNum,
    AB.AddrStreet,
    AB.AddrCity,
    AB.AddrState,
    AB.AddrZipCode,
    AB.YearBuilt,
    AvailableUnits.NumberOfAvailableUnits,
    A.aType AS AmenityType,
    A.Description AS AmenityDescription
FROM
    ApartmentBuilding AB
    LEFT JOIN (
        SELECT
            CompanyName,
            BuildingName,
            COUNT(*) AS NumberOfAvailableUnits
        FROM
            ApartmentUnit
        WHERE
            AvailableDateForMoveIn > CURRENT_DATE
        GROUP BY
            CompanyName, BuildingName
    ) AS AvailableUnits ON AB.CompanyName = AvailableUnits.CompanyName AND AB.BuildingName = AvailableUnits.BuildingName
    LEFT JOIN Provides P ON AB.CompanyName = P.CompanyName AND AB.BuildingName = P.BuildingName
    LEFT JOIN Amenities A ON P.aType = A.aType
WHERE
    AB.BuildingName = 'BuildingX'
ORDER BY -- can be removed to make more efficient.
    AB.CompanyName,
    AB.BuildingName,
    A.aType;

--search by unit
SELECT 
    AB.CompanyName,
    AB.BuildingName,
    AB.AddrNum,
    AB.AddrStreet,
    AB.AddrCity,
    AB.AddrState,
    AB.AddrZipCode,
    AB.YearBuilt,
    AU.UnitRentID,
    AU.unitNumber,
    AU.MonthlyRent,
    AU.squareFootage,
    AU.AvailableDateForMoveIn,
    PA.aType AS AmenityType,
    A.Description AS AmenityDescription
FROM 
    ApartmentUnit AU
INNER JOIN 
    ApartmentBuilding AB ON AU.CompanyName = AB.CompanyName AND AU.BuildingName = AB.BuildingName
LEFT JOIN 
    Provides PA ON AB.CompanyName = PA.CompanyName AND AB.BuildingName = PA.BuildingName
LEFT JOIN 
    Amenities A ON PA.aType = A.aType
WHERE 
    AU.unitNumber = '104';