curl -d '{  "first_name":"Lucas",  "last_name":"Hernanadez",  "uin":659982167,  "gpa":2.96,  "partner_first_name":"Chris",  "partner_last_name":"Dowd",  "partner_gpa":3.21,  "prefs":[0, 0, 2, 3, 2, 3, 0, 0],}'  -H "Content-Type: application/json" -X GET http://localhost:5000/StudentPreferenceData
curl -X GET http://localhost:5000/StudentList
