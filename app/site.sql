CREATE TABLE Users (
    userId int PRIMARY KEY,
    username varchar(16) NOT NULL,
    passwordHash  varchar(255) NOT NULL,
    lastName varchar(32),
    firstName varchar(32),
    addressID_FK int
);

CREATE TABLE Addresses (
    addressID int PRIMARY KEY,
    streetName varchar(255),
    streetNumber varchar(10),
    postcode varchar(10),
    city varchar(32),
    state varchar(32),
    country varchar(255),
    latitude real DEFAULT NULL,
    longitude real DEFAULT NULL
);

CREATE TABLE Posts (
    postId int PRIMARY KEY,
    userId_FK int NOT NULL,
    itemName varchar(255),
    itemDescription varchar(Max)
    image1_FK int,
    image2_FK int,
    image3_FK int,
    image4_FK int,
    image5_FK int
);

CREATE TABLE Images (
    imageId int PRIMARY KEY,
    imageData BLOB
);

CREATE TABLE Replies (
    replyId int PRIMARY KEY,
    userId_FK int NOT NULL,
    postId_FK int NOT NULL,
    msg varchar(Max)
);
