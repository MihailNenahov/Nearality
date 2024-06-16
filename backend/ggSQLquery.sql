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
password varchar(30) not null,
id_location int not null
)

create	table smilies(
id_smilies serial primary key,
id_sender int not null,
id_received int not null
)

	
---------------
drop table locations

alter table user_info drop constraint fk_user_info_id_location

alter table chat drop constraint fk_user_info_chat
	
drop table user_info

drop table smilies	
------------------------

	
INSERT INTO smilies (id_sender,id_received) VALUES (6,7);

INSERT INTO smilies (id_sender,id_received) VALUES (11,7);

INSERT INTO smilies (id_sender,id_received) VALUES (9,7);

INSERT INTO smilies (id_sender,id_received) VALUES (8,7);

INSERT INTO smilies (id_sender,id_received) VALUES (12,7);

INSERT INTO smilies (id_sender,id_received) VALUES (5,7);

select * from smilies

	
	
INSERT INTO locations (name) VALUES ('Zuowska 22, 736 Warszawa');
	
INSERT INTO locations (name) VALUES ('byterbrod 339, 228 Warszawa');
	
INSERT INTO locations (name) VALUES ('shaurma 73, 36 Warszawa');
	
INSERT INTO locations (name) VALUES ('superpuper 34, 667 Warszawa');

select * from locations

	

insert into user_info(name,id_location,password) 
values ('pavel','1','pass');

insert into user_info(name,id_location,password) 
values ('mihail','2','pass');

insert into user_info(name,id_location,password) 
values ('alejandro','3','pass');

insert into user_info(name,id_location,password) 
values ('mustafa','4','pass');

insert into user_info(name,id_location,password) 
values ('Bobr','1','pass');

insert into user_info(name,id_location,password) 
values ('Chuvak','2','pass');

insert into user_info(name,id_location,password) 
values ('Viney','3','pass');

insert into user_info(name,id_location,password) 
values ('Aladin','4','pass');

select * from user_info

ALTER TABLE user_info
ADD CONSTRAINT fk_user_info_id_location
FOREIGN KEY (id_location)
REFERENCES locations (id_location);

ALTER TABLE smilies
ADD CONSTRAINT fk_user_info_smilies
FOREIGN KEY (id_sender)
REFERENCES user_info (id_user_info);

ALTER TABLE smilies
ADD CONSTRAINT fk_user_info_smilies_r
FOREIGN KEY (id_received)
REFERENCES user_info (id_user_info);

