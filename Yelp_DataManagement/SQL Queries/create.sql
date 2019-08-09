create database Yelp;
use Yelp;

create table business(
    address varchar(200),
	business_id varchar(200) Primary key,
    city varchar(300),
    is_open int,
    latitude float,
    longitude float,
    name varchar(500) CHARACTER SET utf8,
    postal_code varchar(50),
    review_count int,
    stars float,
    state varchar(50)
);

create table user(
	average_stars float,
	compliment_cool	int,
    compliment_cute	int,
    compliment_funny int,
    compliment_hot int,
	compliment_list	int,
    compliment_more int,
    compliment_note	int,
    compliment_photos int,
    compliment_plain int,
	compliment_profile int,
	compliment_writer int,
	cool int,
    fans int,
    funny int,
    name varchar(1000) CHARACTER SET utf8,
    review_count int,
    useful int,
    user_id varchar(22) primary key,
    yelping_since varchar(80)
);

CREATE TABLE Reviews(
    business_id varchar(22),
    cool int,
    funny int,
	review_id varchar(22) primary key,
    date varchar(30),
    text blob,
    stars int, 
    useful int,
    user_id varchar(22),
	foreign key(business_id) references business(business_id),
    foreign key(user_id) references user(user_id)    
);
    
create table Tip(
    business_id varchar(22),
    compliment_count int,
    date varchar(50),
	text varchar(5000) CHARACTER SET utf8,
    user_id varchar(22),
    foreign key(business_id) references business(business_id),
    foreign key(user_id) references user(user_id)
);

create table checkin_count(
	business_id varchar(22),
	number_of_checkins int,
	foreign key(business_id) references business(business_id)
);

create table photo(
	business_id varchar(22),
    caption varchar(500) CHARACTER SET utf8,
	label varchar(100),
    photo_id varchar(22) primary key,
    foreign key(business_id) references business(business_id)
);

create table hours(
	business_id varchar(22),
    hours_Friday varchar(40),
    hours_Monday varchar(40),
    hours_Saturday varchar(40),
    hours_Sunday varchar(40),
    hours_Thursday varchar(40),
    hours_Tuesday varchar(40),
    hours_Wednesday varchar(40),
	foreign key(business_id) references business(business_id)
);

create table categories(
	business_id varchar(22),
    categories varchar(100),
    foreign key(business_id) references business(business_id)
);