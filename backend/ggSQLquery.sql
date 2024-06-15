create user pavel password '12345';
grant all on database nearality0 to pavel;
alter user pavel with createrole;

select *
from pg_shadow

CREATE TABLE locations (
    id_location SERIAL PRIMARY KEY,
    name VARCHAR(100) not null
);

create	table user_info(
id_user_info serial primary key,
name varchar(20) not null,
id_location int not null
)

create	table chat(
id_user_info int not null,
message varchar(200) not null
)
	
---------------
drop table locations

alter table user_info drop constraint fk_user_info_id_location
	
drop table user_info
------------------------

	
INSERT INTO locations (name) VALUES ('Zuowska 22, 736 Warszawa');
	
INSERT INTO locations (name) VALUES ('byterbrod 339, 228 Warszawa');
	
INSERT INTO locations (name) VALUES ('shaurma 73, 36 Warszawa');
	
INSERT INTO locations (name) VALUES ('superpuper 34, 667 Warszawa');

select * from locations

insert into user_info(name,id_location) 
values ('pavel','1');

insert into user_info(name,id_location) 
values ('mihail','2');

insert into user_info(name,id_location) 
values ('alejandro','3');

insert into user_info(name,id_location) 
values ('mustafa','4');

select * from user_info

ALTER TABLE user_info
ADD CONSTRAINT fk_user_info_id_location
FOREIGN KEY (id_location)
REFERENCES locations (id_location);


ALTER TABLE chat
ADD CONSTRAINT fk_user_info_chat
FOREIGN KEY (id_user_info)
REFERENCES user_info (id_user_info);

select * from tester
