create database demo;
create table employees
(
   id integer not null,
   first_name varchar(255) not null, 
   last_name varchar(255) not null,
   email_address varchar(255) not null,
   primary key(id)
);
create table value_info
(
   id integer not null,
   `value` integer not null,
   primary key(id)
);