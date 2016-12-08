INSERT INTO modules(address, type, location) VALUES('192.168.100.150', 'arduino ethernet', 'chambre');
INSERT INTO modules(address, type, location) VALUES('192.168.100.150', 'arduino ethernet', 'chambre');
INSERT OR IGNORE INTO modules(address, type, location) VALUES('192.168.100.150', 'arduino ethernet', 'chambre');
INSERT OR IGNORE INTO modules(address) VALUES('192.168.100.150');

delete from modules where id = 1;
select * from modules;

insert into temperatures(id_Module,temperature,time) select ID, '13', '153023' from modules where address='192.168.100.150';

select id_module,temperature from temperatures inner join modules where id_module = modules.id and address='192.168.100.139';

# obselete line
INSERT INTO modules(address) SELECT * FROM (SELECT '192.168.100.150') AS tmp WHERE NOT EXISTS ( SELECT address FROM modules WHERE address = '192.168.100.150') LIMIT 1;
