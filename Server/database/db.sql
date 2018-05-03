CREATE TABLE campus
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE building
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    campus INT NOT NULL,
    CONSTRAINT campus_fk FOREIGN KEY (campus) REFERENCES Campus (id)
);

CREATE TABLE room
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    type INT NOT NULL,
    room_num INT NOT NULL,
    building INT NOT NULL,
    CONSTRAINT buildingfk FOREIGN KEY (building) REFERENCES Building (id)
);

CREATE TABLE user
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    prefix INT NOT NULL,
    office INT NOT NULL,
    CONSTRAINT room___fk FOREIGN KEY (office) REFERENCES Room (id)
);
CREATE TABLE class
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    crn INT NOT NULL,
    section INT NOT NULL,
    start DATETIME NOT NULL,
    end DATETIME NOT NULL,
    professor INT NOT NULL,
    room_num INT NOT NULL,
    CONSTRAINT professorfk FOREIGN KEY (professor) REFERENCES User (id),
    CONSTRAINT classroomfk FOREIGN KEY (room_num) REFERENCES Room (id)
);

CREATE TABLE office_hours
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    start DATETIME NOT NULL,
    end DATETIME NOT NULL,
    professor INT NOT NULL,
    room_num INT NOT NULL,
    CONSTRAINT professor_hours_fk FOREIGN KEY (professor) REFERENCES User (id),
    CONSTRAINT officenumfk FOREIGN KEY (room_num) REFERENCES Room (id)
);

CREATE TABLE event
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    host VARCHAR(255) NOT NULL,
    image BLOB,
    start DATETIME NOT NULL,
    end DATETIME NOT NULL,
    room_num INT NOT NULL,
    CONSTRAINT event_room_fk FOREIGN KEY (room_num) REFERENCES Room (id)
);

CREATE TABLE announcement
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    info TEXT NOT NULL,
    image BLOB,
    professor INT NOT NULL,
    room_num INT NOT NULL,
    CONSTRAINT professorannfk FOREIGN KEY (professor) REFERENCES User (id),
    CONSTRAINT ann_room___fk FOREIGN KEY (room_num) REFERENCES Room (id)
);