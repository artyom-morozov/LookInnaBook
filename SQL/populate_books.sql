delete from book;
delete from author;
delete from publisher;

-- Book 1
insert into author(ID, name) values ('1001', 'Jane Austen');
insert into publisher(ID, name, email, address, phone_number, bank_account) values ('1021', 'Penguin Classics', 'penguin@penguin.com', '23 North York Street, London, UK', '+1(613)1312341', '1723712636');
insert into book(ID, authorID, publisherID, title, ISBN, price, genre, page_num, publisher_percentage, inventory_quantity ) values ('1031', '1001', '1021', 'Pride and Prejudice', '9780141199078', '23.00', 'Drama', '416', '11', '256');

-- Book 2
insert into author(ID, name) values ('1002', 'Harper Lee');
insert into book(ID, authorID, publisherID, title, ISBN, price, genre, page_num, publisher_percentage, inventory_quantity ) values ('1032', '1002', '1021', 'To Kill a Mockingbird ', '9781784752637', '26.00', 'Drama', '320  ', '10', '500');

-- Book 3
insert into author(ID, name) values ('1003', 'Aldous Huxley');
insert into publisher(ID, name, email, address, phone_number, bank_account) values ('1023', 'Vintage Classics', 'vintage@classic.com', '23 West York Street, London, UK', '+1(613)1516341', '3123123');
insert into book(ID, authorID, publisherID, title, ISBN, price, genre, page_num, publisher_percentage, inventory_quantity ) values ('1033', '1003', '1023', 'Brave New World', '9781784870140', '9.99', 'Drama', '288', '12', '100');