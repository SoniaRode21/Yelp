import pandas as pd # pandas is used to read csv files
import MySQLdb # MySQLdb is used to connect Python with MySQL
import csv, sys

csv.field_size_limit(sys.maxsize)

def connect_to_db(host, user, password, database):
	db = MySQLdb.connect(host=host,
    					user=user,
    					passwd=password,
    					db=database)
	db.set_character_set('utf8')
	return db

def parse_db():
	
	business = pd.read_csv("./data/business.csv", engine='python')
	business = business.drop(['attributes','attributes_AcceptsInsurance','attributes_AgesAllowed','attributes_Alcohol','attributes_Ambience','attributes_BYOB','attributes_BYOBCorkage','attributes_BestNights','attributes_BikeParking','attributes_BusinessAcceptsBitcoin','attributes_BusinessAcceptsCreditCards','attributes_BusinessParking','attributes_ByAppointmentOnly','attributes_Caters','attributes_CoatCheck','attributes_Corkage','attributes_DietaryRestrictions','attributes_DogsAllowed','attributes_DriveThru','attributes_GoodForDancing','attributes_GoodForKids','attributes_GoodForMeal','attributes_HairSpecializesIn','attributes_HappyHour','attributes_HasTV','attributes_Music','attributes_NoiseLevel','attributes_Open24Hours','attributes_OutdoorSeating','attributes_RestaurantsAttire','attributes_RestaurantsCounterService','attributes_RestaurantsDelivery','attributes_RestaurantsGoodForGroups','attributes_RestaurantsPriceRange2','attributes_RestaurantsReservations','attributes_RestaurantsTableService','attributes_RestaurantsTakeOut','attributes_Smoking','attributes_WheelchairAccessible','attributes_WiFi'],axis=1)
	business = business.drop(['categories','hours','hours_Friday','hours_Monday','hours_Saturday','hours_Sunday','hours_Thursday','hours_Tuesday','hours_Wednesday'], axis=1)
	business = business.dropna()
	return business

business_db = parse_db()

def create_MySQL_table(db, tableName, dataframe, verbose = False):
    """
    db: MySQLdb connection
    tableName: the name of the table to be created in MySQL
    dataframe: the dataframe read from the .csv file
    verbose: will print the generated sql command if True
    """
    cursor = db.cursor()
   
    # insert the values into the table
    colStr = "" # generate a string of column names separated by ", "
    for colName in dataframe.columns:
        colStr += colName + ","
    colStr = colStr.strip(",")
    for row in dataframe.iterrows():
    	sql = "INSERT INTO " + tableName + " (" + colStr + ") VALUES ("
    	formatStr = ""; valueStr = ""
    	sql += ", ".join(str(row[1].values).strip("[]").split(' ')) + ")"
    	print(sql)
    	cursor.execute(sql) 
    	db.commit()
   

def main():
	host = '35.193.29.72'																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																		
	user = 'unagi'
	password = 'unagi@123'
	database = 'Yelp'
	db = connect_to_db(host, user, password, database)     

	create_MySQL_table(db, "business", business_db, verbose = False)	

	cursor = db.cursor()
	cursor.fetchall()

if __name__ == '__main__':
    main()