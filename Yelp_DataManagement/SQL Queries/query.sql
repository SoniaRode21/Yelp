use Yelp;

# QUERY 1: GROUP BUSINESSES IN A PARTICULAR AREA BASED ON THEIR STAR RATING
	SELECT DISTINCT name,stars,address,postal_code 
 	FROM business  
 	WHERE city="Toronto" 
 	AND stars=4 
 	LIMIT 50;

# QUERY 2: BUSINESSES/RESTAURANTS OPEN AT A GIVEN TIME
	
	SELECT distinct name 
	FROM business,hours,categories
	WHERE business.business_id=hours.business_id 
	AND business.business_id=categories.business_id 
	AND hours_Friday="7:0-1:0" AND categories LIKE "%Restaurants%";	

	#Options for hours on hours_Monday, hours_Tuesday, etc 
	#Options for different categories : Restaurants, shopping, salons, bars
	#Options for hours : 10:0-1:0, 10:0-18:0, 11:30-19:0, 15:30-17:30, 8:30-23:30

# QUERY 3: Top 10 users based on the review_count.
	SELECT name, max(review_count) AS review_count 
	FROM user
	GROUP BY name 
	ORDER BY review_count DESC
	LIMIT 10;

# QUERY 4: Top 15 Businesses with maximum no. of checkin
	SELECT b.name,b.address,b.city,max(number_of_checkins) AS checkin_count
	FROM business AS b,checkin_count
	WHERE b.business_id = checkin_count.business_id
	GROUP BY checkin_count.business_id
	ORDER BY checkin_count DESC
	LIMIT 15;

# QUERY 5: Top 50 most review businesses with categories=Restaurants/Shopping/Fashion.
	SELECT  business.name, business.city, business.review_count, business.stars   
	FROM business   
	INNER JOIN categories ON business.business_id = categories.business_id   
	WHERE categories.categories = "Shopping"   
	ORDER BY business.review_count DESC  
	LIMIT 50;

# QUERY 6: Get count of businesses of a particular category per city	
	SELECT  business.city, COUNT(*) AS 'Number of Restaurants per City'	
	FROM business	
	INNER JOIN categories on business.business_id = categories.business_id	
	WHERE categories.categories = "Restaurants"	
	GROUP BY business.city order by count(*) desc
	LIMIT 50;	

# Options for different categories : Restaurants, shopping, salons, bars

# QUERY 7: Categories having highest total count of reviews 
	SELECT  sum(review_count),categories.categories
	FROM business, categories 
	WHERE business.business_id=categories.business_id
	GROUP BY categories.categories
	ORDER BY sum(review_count) DESC
	LIMIT 50;

# QUERY 8: All users who have not been satisfied by service of a given business
	SELECT user.name AS USERNAME, business.name AS BUSINESS_NAME, Reviews.stars AS STARS_GIVEN
	FROM business, user, Reviews
	WHERE business.business_id = Reviews.business_id AND Reviews.user_id =user.user_id
	AND Reviews.stars < 2 AND business.name="IHOP"; 

	# Options for name -- IHOP, Starbucks, Sushiya, KFC, etc.

# QUERY 9: Top 10 users based on popularity.(no_of_fans)
	SELECT name, max(fans) AS no_of_fans  
	FROM user
	GROUP BY name 
	ORDER BY no_of_fans DESC LIMIT 10 ;

# QUERY 10: Listing names of restaurants that have menu photos
 	SELECT DISTINCT business.name 
 	FROM photo, business, categories
 	WHERE business.business_id = photo.business_id AND business.business_id= categories.business_id
 	AND label ='menu' AND categories.categories LIKE '%Restaurants%' 
    LIMIT 50;

# QUERY 11: Number of tips grouped according to the date posted 
	SELECT extract(year FROM date) AS year, MONTHNAME(date) AS month, 
	count(*) AS Number_of_tips
	FROM Tip AS t 
	GROUP BY year, month
	ORDER BY year DESC, count(*) DESC;
    
# Query 12 : Trigger for insertion of row in Reviews table and increments the review_count in the business table by 1.

	delimiter |
	create trigger ReviewCountIncrement 
	AFTER INSERT 
	on 
	Reviews 
	for each row 
	BEGIN
		UPDATE business SET review_count = review_count + 1 WHERE business_id = NEW.business_id;
 	END;
 	|
	delimiter ;

	insert into Reviews values ("123",3,4,"abc1","2018-02-02, 10:03:06","Good Food.",4,4,"abc");

# Query 13 : Top businesses with cool rated reviews
	SELECT b.name 
	FROM business AS b 
	WHERE b.business_id in (SELECT r.business_id 
							FROM Reviews AS r
							GROUP BY r.business_id HAVING SUM(r.cool) > 20
							ORDER BY sum(r.cool)  DESC);
