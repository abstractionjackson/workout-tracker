BASE_URL="http://localhost:5000"

curl -X POST -H "Content-Type: application/json" -d '{
    "email": "johndoe@example.com",
    "password": "secretpassword"
}' $BASE_URL/auth/register
