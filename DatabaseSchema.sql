drop table User cascade constraints;
drop table BusRoutes cascade constraints;
drop table UserPrefHist cascade constraints;
drop table PoribohonRoutes cascade constraints;
drop table PlaceLocs cascade constraints;
drop table HubLocs cascade constraints;
drop table Review cascade constraints;
drop table LogData cascade constraints;
drop table SignInOutLog cascade constraints;

create table User(
  userId varchar(15) not null,
  username varchar(250) not null,
  password varchar(250) not null,
  email varchar(500) not null,
  firstname varchar(500) not null,
  lastname varchar(500) not null,
  primary key(userId)
);

create table BusRoutes(
  busId varchar(15) not null,
  place varchar(250) not null,
  _values varchar(500) not null,
  roads varchar(500) not null,
  geoLocLat number not null,
  geoLocLon number not null,
  primary key(busId)
);

create table UserPrefHist(
  uprefId varchar(15) not null,
  UserName varchar(250) not null,
  preferredRoutes varchar(500) not null,
  history varchar(500) not null,
  primary key(uprefId)
);

create table PoribohonRoutes(
  poribohonId varchar(15) not null,
  poribohonName varchar(250) not null,
  fullRoute varchar(500) not null,
  imgLink varchar(300) not null,
  primary key(poribohonId)
);

create table PlaceLocs(
  placeId varchar(15) not null,
  placeName varchar(250) not null,
  geoLocLat number not null,
  geoLocLon number not null,
  primary key(placeId)
);

create table HubLocs(
  hubId varchar(15) not null,
  hubName varchar(250) not null,
  geoLocLat number not null,
  geoLocLon number not null,
  primary key(hubId)
);

create table Review(
  reviewId varchar(15) not null,
  uName varchar(15) not null,
  poribohon varchar(15) not null,
  comment varchar(500) not null,
  primary key(reviewId),
  foreign key(uName) references User(userId),
  foreign key(poribohon) references PoribohonRoutes(poribohonId)
);

create table LogData(
  logdataId varchar(15) not null,
  uName varchar(15) not null,
  logType varchar(250) not null,
  details varchar(500) not null,
  primary key(logdataId),
  foreign key(uName) references User(userId)
);

create table SignInOutLog(
  signinoutId varchar(15) not null,
  uName varchar(15) not null,
  details varchar(500) not null,
  primary key(signinoutId),
  foreign key(uName) references User(userId)
);

insert into User	values ('u-001',	'sam', 'password_1','sam@xyz.com','sam','smith');
insert into User	values ('u-002',	'turner', 'password_2','turner@xyz.com','turner','peters');
insert into User	values ('u-003',	'gary', 'password_3','gary@xyz.com','gary','alters');
insert into User	values ('u-004',	'alice', 'password_4','alice@xyz.com','alice','jones');

insert into BusRoutes	values ('br-001',	'Dhanmondi-15', 'Zigatola_Bolaka,Farmgate_Bahon','Zigatola,Dhanmondi-27',23.59021,90.68921);
insert into BusRoutes	values ('br-002',	'Farmgate', 'Zigatola_Bolaka,Dhanmondi-15_Bahon','Bijoy Shoroni,Dhanmondi-27',23.8971,90.32921);

insert into UserPrefHist	values ('uph-001',	'sam', 'Badda to Uttara,Farmgate to Motijheel','Badda to Dhanmondi-15,Rampura to Shahbag');
insert into UserPrefHist	values ('uph-002',	'turner', 'Farmgate to Uttara,Shahbag to Basundhora','Motijheel to Dhanmondi-15');

insert into PoribohonRoutes	values ('pr-001',	'Akik', 'Zigatola,Farmgate,Shahbag','/static/Akik.jpg');
insert into PoribohonRoutes	values ('pr-002',	'Suprovat', 'Basundhora,Badda,Rampura','/static/Suprovat.jpg');

insert into PlaceLocs	values ('pl-001',	'Satmasjid Road', 23.59021,90.68921);
insert into PlaceLocs	values ('pl-002',	'Paltan', 23.8971,90.32921);

insert into HubLocs	values ('hl-001',	'Farmgate', 24.59021,91.68921);
insert into HubLocs	values ('hl-002',	'Motijheel', 24.8971,92.32921);

insert into Review	values ('r-001',	'u-001', 'pr-001','very good');
insert into Review	values ('r-002',	'u-002', 'pr-002','satisfactory');

insert into LogData	values ('lg-001',	'u-001', 'searched-route','sam searched routes for Farmgate to Motijheel');
insert into LogData	values ('lg-002',	'u-002', 'viewed-history','turner viewed history');

insert into LogData	values ('sio-001',	'u-001','sam logged in');
insert into LogData	values ('sio-002',	'u-002', 'turner logged out');
