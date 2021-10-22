CREATE TABLE 'Entries' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'concept' TEXT NOT NULL,
    'entry' TEXT NOT NULL,
    'mood_id' INTEGER NOT NULL,
    FOREIGN KEY ('mood_id') REFERENCES 'Mood'('id')
);

CREATE TABLE 'Mood' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'label' TEXT NOT NULL
);

INSERT INTO 'Mood' VALUES (null, "Happy");
INSERT INTO 'Mood' VALUES (null, "Sad");
INSERT INTO 'Mood' VALUES (null, "Angry")


INSERT INTO 'Entries' VALUES(null, "Javascript", "test entry text", 2);
INSERT INTO 'Entries' VALUES(null, "React", "test entry", 1);

SELECT label
FROM Mood