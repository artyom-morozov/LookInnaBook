create table author
	(
    ID	SERIAL,
    name		varchar(35),
	primary key (ID)
	);

create table publisher
	(ID	SERIAL, 
	 name		varchar(35), 
	 email		        varchar(20),
     address varchar(50),
     phone_number varchar(35),
     bank_account varchar(35),
	 primary key (ID)
	);

create table book
	(ID	SERIAL, 
    authorID		integer,
    publisherID		integer,
	 title			varchar(50), 
	 ISBN		varchar(20),
	 price		numeric(10,2),
     genre varchar(20),
     page_num numeric(5, 0),
    publisher_percentage numeric(2, 0),
    inventory_quantity numeric(10, 0),
	 primary key (ID),
     foreign key (authorID) references author,
	 foreign key (publisherID) references publisher
	);

create table customer
	( name		varchar(20),
	 email			varchar(20), 
	 password		varchar(35),
     bank_account varchar(35),
	 primary key (name)
	);

create table full_order
	(ID		SERIAL, 
    customer_name		varchar(20), 
     billing_address varchar(50),
     shipping_address varchar(50),
     total		numeric(20,2),
	 primary key (ID),
	 foreign key (customer_name) references customer
	);

create table book_order
	(
    orderID		integer, 
    bookID     integer,
	 foreign key (bookID) references book,
     foreign key (orderID) references full_order,
     quantity numeric(10, 0),
     primary key(bookID, orderID)
	);