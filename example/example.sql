create table test.minifw
(
	id int not null auto_increment
		primary key,
	name varchar(200) null,
	constraint minifw_id_uindex
		unique (id)
)
;

