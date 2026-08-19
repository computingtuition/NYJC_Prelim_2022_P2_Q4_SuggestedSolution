SELECT Person.name, Record.Time
FROM Person, Record
WHERE Record.visitorId = Person.id
AND Record.Time > "0730"
AND Record.Type = "entry"
AND Person.Role = "Student"
ORDER BY Record.Date ASC, Record.Time ASC