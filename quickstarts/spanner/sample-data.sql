insert into Players (playerUUID, player_name, email, password_hash, created)
values('000b1bc7-173e-48e1-90c8-fbab8ebd9b2c', 'Koala Boy', 'koalaboy@mydomain.com',FROM_BASE64('BAR'), current_timestamp());


insert into Players (playerUUID, player_name, email, password_hash, created)
values('000dc4af-b4ef-4878-a798-51a8a900fed6', 'Koala Girl', 'koalagirl@mydomain.com',FROM_BASE64('BAR'), current_timestamp());


insert into Sessions (sessionUUID) values ('000ee21c-034c-4199-9a07-e5ba28c52631');
insert into Sessions (sessionUUID, players, created)
values ('001293ff-bff1-49c6-8a21-700bb486b3ed', ARRAY_CONCAT(['000b1bc7-173e-48e1-90c8-fbab8ebd9b2c', '000dc4af-b4ef-4878-a798-51a8a900fed6']),current_timestamp() );


insert into SessionRanking (sessionUUID, playerUUID, score) values ('001293ff-bff1-49c6-8a21-700bb486b3ed', '000b1bc7-173e-48e1-90c8-fbab8ebd9b2c', 88);
insert into SessionRanking (sessionUUID, playerUUID, score) values ('001293ff-bff1-49c6-8a21-700bb486b3ed', '000dc4af-b4ef-4878-a798-51a8a900fed6', 54);


insert into InAppPurchase (playerUUID ,sessionUUID, purchaseUUID, purchase_total_price,created, purchaseLog) values
('000b1bc7-173e-48e1-90c8-fbab8ebd9b2c', '001293ff-bff1-49c6-8a21-700bb486b3ed', '011c042c-6607-492e-881a-ca8046fffded', 124.9, current_timestamp(),FROM_BASE64('weapon1') )
