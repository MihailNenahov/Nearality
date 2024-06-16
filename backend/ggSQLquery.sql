create user pavel password '12345';
grant all on database nearality0 to pavel;
alter user pavel with createrole;

select *
from pg_shadow

CREATE TABLE locations (
    id_location SERIAL PRIMARY KEY,
    name VARCHAR(100) not null
);

update user_info set id_location = ? where id_user_info = ?

SELECT * FROM user_info WHERE id_location = 1

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

create	table chat(
id_user_info int,
message varchar(200) not null
)
	
---------------
drop table locations

alter table user_info drop constraint fk_user_info_id_location

alter table chat drop constraint fk_user_info_chat
	
drop table user_info

drop table smilies	

TRUNCATE TABLE smilies

------------------------

	
INSERT INTO smilies (id_sender,id_received) VALUES (6,7);

INSERT INTO smilies (id_sender,id_received) VALUES (11,7);

INSERT INTO smilies (id_sender,id_received) VALUES (9,7);

INSERT INTO smilies (id_sender,id_received) VALUES (8,7);

INSERT INTO smilies (id_sender,id_received) VALUES (12,7);

INSERT INTO smilies (id_sender,id_received) VALUES (16,14);

INSERT INTO smilies (id_sender,id_received) VALUES (14,16);

delete from user_info where id_user_info in (7,5,8);
delete from smilies where id_sender in (7,5,8) and id_received in (7,5,8);

	commit;
	
INSERT INTO locations (name) VALUES ('Zuowska 22, 736 Warszawa');
	
INSERT INTO locations (name) VALUES ('byterbrod 339, 228 Warszawa');
	
INSERT INTO locations (name) VALUES ('shaurma 73, 36 Warszawa');
	
INSERT INTO locations (name) VALUES ('superpuper 34, 667 Warszawa');

select * from locations

insert into user_info(name,id_location,password) 
values ('Oleg','1','pass');

insert into user_info(name,id_location,password) 
values ('Leon','1','pass');

insert into user_info(name,id_location,password) 
values ('Grigoriy','1','pass');

insert into user_info(name,id_location,password) 
values ('Mrigoriy','1','pass');



	
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

ALTER TABLE chat
ADD CONSTRAINT fk_chat_user_info
FOREIGN KEY (id_user_info)
REFERENCES user_info (id_user_info);
