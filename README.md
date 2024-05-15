
curl -d '{"student_name":"test", "student_age" : 33 }' -H "Content-Type: application/json" 'localhost/student-server/insert' 

curl 'localhost/student-server/select/<id>' 
