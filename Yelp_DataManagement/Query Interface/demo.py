from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'Yelp'
app.config['MYSQL_HOST'] = '35.193.29.72'

mysql = MySQL(app)

user_id = [10]

headerNames = {
1: ['Name', 'Stars', 'Address', 'Postal code'],
2: ['Name'],
3: ['Name', 'Review count'],
4: ['Name', 'Address', 'City', 'Checkin count'],
5: ['Name', 'City', 'Review count', 'Stars'],
6: ['City', 'Number of Restaurants per city'],
7: ['Total (review count)', 'Categories'],
8: ['Username', 'Business name', 'Stars given'],
9: ['Name', 'No. of fans'],
10: ['Name'],
11: ['Year', 'Month', 'No. of tips'],
12: ['Review_count']
}

queryList = {
    1: '''SELECT distinct name,stars,address,postal_code 
 	from business  
 	where city="Toronto" 
 	and stars=4 
 	LIMIT 50;''',

    2: '''SELECT distinct name 
	from business,hours,categories
	where business.business_id=hours.business_id 
	and business.business_id=categories.business_id 
	and hours_Friday="7:0-1:0" and categories like "%Restaurants%";''',

    3: '''select name, max(review_count) as review_count 
	from user
	group by name 
	order by review_count desc limit 10;''',

    4: '''select b.name,b.address,b.city,max(number_of_checkins) as checkin_count
	from business as b,checkin_count
	where b.business_id = checkin_count.business_id
	group by checkin_count.business_id
	order by checkin_count desc
	limit 15;''',

    5: '''select  business.name, business.city, business.review_count, business.stars   
	from business   
	inner join categories on business.business_id = categories.business_id   
	where categories.categories = "Shopping"   
	order by business.review_count desc   
	limit 50;''',

    6: '''SELECT  business.city, COUNT(*) AS "Number of Restaurants per City"	
	FROM business	
	INNER JOIN categories on business.business_id = categories.business_id	
	WHERE categories.categories = "Restaurants"	
	GROUP BY business.city order by count(*) desc;''',

    7: '''SELECT  sum(review_count),categories.categories
	from business, categories 
	where business.business_id=categories.business_id
	group by categories.categories
	order by sum(review_count) desc
	limit 50;''',

    8: '''Select user.name as USERNAME, business.name as BUSINESS_NAME, Reviews.stars as STARS_GIVEN
	From business, user, Reviews
	Where business.business_id = Reviews.business_id and Reviews.user_id =user.user_id
	and Reviews.stars < 2 and business.name="IHOP";''',

    9: '''select name, max(fans) as no_of_fans  
	from user
	group by name 
	order by no_of_fans desc limit 10 ;''',

    10: '''Select distinct business.name 
 	from photo, business, categories
 	where business.business_id = photo.business_id and business.business_id= categories.business_id
 	and label ='menu' and categories.categories LIKE '%Restaurants%'
Limit 50;''',

    11: '''select extract(year from date) as year, MONTHNAME(date) as month, 
count(*) as Number_of_tips
from Tip as t
group by year, month
order by year desc, count(*) desc;''',

    12: '''select review_count from business where business_id="123";'''
}

@app.route("/")

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/query", methods=['POST'])
def query():
    selectedQueryNumber = request.form['options']
    updateQueryNo = [1, 2, 5, 6, 8, 12]
    cur = mysql.connection.cursor()
    new_user = user_id[0]
    if int(selectedQueryNumber) in updateQueryNo:
        if selectedQueryNumber == '1':
            city = request.form[selectedQueryNumber]
            query = '''SELECT distinct name,stars,address,postal_code from business where city="''' + city + '''" and stars=4 LIMIT 50;'''
            queryList[int(selectedQueryNumber)] = query

        elif selectedQueryNumber == '2':
            categories = request.form[selectedQueryNumber]
            query = '''SELECT distinct name from business,hours,categories where business.business_id=hours.business_id and business.business_id=categories.business_id  and hours_Friday="7:0-1:0" and categories like "%''' + categories + '''%";'''
            queryList[int(selectedQueryNumber)] = query

        elif selectedQueryNumber == '5':
            categories = request.form[selectedQueryNumber]
            query = '''select  business.name, business.city, business.review_count, business.stars from business inner join categories on business.business_id = categories.business_id where categories.categories = "''' + categories + '''" order by business.review_count desc limit 50;'''
            queryList[int(selectedQueryNumber)] = query

        elif selectedQueryNumber == '6':
            categories = request.form[selectedQueryNumber]
            query = '''SELECT  business.city, COUNT(*) AS "Number of Restaurants per City" FROM business INNER JOIN categories on business.business_id = categories.business_id	WHERE categories.categories = "''' + categories + '''" GROUP BY business.city order by count(*) desc;'''
            queryList[int(selectedQueryNumber)] = query

        elif selectedQueryNumber == '8':
            businessName = request.form[selectedQueryNumber]
            query = '''Select user.name as USERNAME, business.name as BUSINESS_NAME, Reviews.stars as STARS_GIVEN From business, user, Reviews Where business.business_id = Reviews.business_id and Reviews.user_id =user.user_id and Reviews.stars < 2 and business.name="''' + businessName + '''";'''
            queryList[int(selectedQueryNumber)] = query

        elif selectedQueryNumber == '12':
            text = request.form[selectedQueryNumber]
            new_user = new_user + 1
            query = '''insert into Reviews values ("123",3,4,"abc''' + str(new_user) + '''","2018-02-02, 10:03:06","''' + text + ''''",4,4," abc");'''
            cur.execute(query)
            mysql.connection.commit()
    user_id[0] = new_user
    cur.execute(queryList[int(selectedQueryNumber)])
    data = cur.fetchall()
    return render_template('querytest.html', data=data, headers=headerNames[int(selectedQueryNumber)])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)