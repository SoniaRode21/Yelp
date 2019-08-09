# Removal of unwanted columns from user
ALTER table user 
DROP COLUMN compliment_cool;

ALTER table user 
DROP COLUMN compliment_cute;

ALTER table user 
DROP COLUMN compliment_funny;

ALTER table user 
DROP COLUMN compliment_hot;

ALTER table user 
DROP COLUMN compliment_list;

ALTER table user 
DROP COLUMN compliment_more;

ALTER table user 
DROP COLUMN compliment_note;

ALTER table user 
DROP COLUMN compliment_photos;

ALTER table user 
DROP COLUMN compliment_plain;
	
ALTER table user 
DROP COLUMN compliment_profile;

ALTER table user 
DROP COLUMN compliment_writer;

# Removal of duplicate business ids
SELECT count(*),name,address,city,state,postal_code 
FROM business 
GROUP BY name,address,postal_code, city,state 
HAVING count(*)>1;

CREATE view dup_business as 
SELECT MIN(review_count) as review_count, name, address, city, state, postal_code 
FROM business 
GROUP BY name,address,postal_code, city,state 
HAVING count(*)>1; 

DELETE from business 
WHERE business_id 
IN (SELECT business_id 
    FROM (select * from business ) as b,dup_business  
	WHERE b.name=dup_business.name 
	AND b.address= dup_business.address 
	AND b.review_count=dup_business.review_count 
    AND b.postal_code=dup_business.postal_code 
	AND b.city=dup_business.city 
	AND b.state=dup_business.state);
    
# TO CHECK DEPENDENCIES OF POSTAL CODE AND CITY
SELECT count(city),postal_code 
FROM business 
GROUP BY postal_code;	

SELECT count(state),postal_code 
FROM business 
GROUP BY postal_code;	

SELECT count(postal_code), latitude, longitude
FROM business
GROUP BY latitude, longitude;

Select * from business where latitude like 51.2942 and longitude like 114.013;

#Normalizing business table for the dependency postal_code -> state by creating a table business1(postal_code, state)
INSERT INTO  business1	
SELECT postal_code,state	
FROM business
