import allure
from tests.helpers import register_user, login_user
from werkzeug.security import generate_password_hash

# TC-13: Register new user

@allure.parent_suite("Authentication tests")
@allure.suite("TC-13: Register new user")
@allure.severity(allure.severity_level.CRITICAL)
class TestRegisterNewUser:

    @allure.sub_suite("Register user with valid data")
    @allure.description("Test registering a new user with valid username, email, and password. Verify that success message is returned, and user can be found in the database.")
    def test_register_user_with_valid_data(self, client, mock_db):
        db = mock_db
        
        username = "username"
        email = "test@example.com"
        password = "password123"

        response = register_user(client, username, email, password)
        assert response.status_code == 201
        response_data = response.get_json()
        assert response_data["msg"] == "User created successfully"

        # Verify user is in the database
        user = list(db["users"].find({"username": username}))
        assert user is not None
        assert len(user) == 1
        assert user[0]["email"] == email


    @allure.sub_suite("Register user with existing username")
    @allure.description("Test registering a new user with a username that already exists in the database. Verify that appropriate error message is returned.")
    def test_register_user_with_existing_username(self, client, mock_db):
        db = mock_db

        existing_username = "existinguser"
        db["users"].insert_one({
            "username": existing_username,
            "email": "existinguser@example.com",
            "password": "password123"
        })

        response = register_user(client, existing_username, "newemail@example.com", "newpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == "Username already exists"


    @allure.sub_suite("Register user with existing email")
    @allure.description("Test registering a new user with an email that is already registered in the database. Verify that appropriate error message is returned.")
    def test_register_user_with_existing_email(self, client, mock_db):
        db = mock_db

        existing_email = "existing@example.com"
        db["users"].insert_one({
            "username": "existingusername",
            "email": existing_email,
            "password": "password123"
        })

        response = register_user(client, "newusername", existing_email, "newpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == "Email already registered"

    
    @allure.sub_suite("Register user with invalid data format")
    @allure.description("Test registering a new user with invalid data formats (short password, invalid email, short username). Verify that appropriate error messages are returned.")
    def test_register_user_with_invalid_data_format(self, client):
        # Test short password
        response = register_user(client, "validusername", "validemail@example.com", "short")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == "Password must be at least 8 characters"

        # Test invalid email format
        response = register_user(client, "validusername", "invalidemail", "validpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == "Invalid email format"

        # Test short username
        response = register_user(client, "u", "validemail@example.com", "validpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == "Username must be from 3 to 20 characters"

    
    @allure.sub_suite("Register user with missing fields")
    @allure.description("Test registering a new user with missing required fields (username, email, password). Verify that appropriate error messages are returned.")
    def test_register_user_with_missing_fields(self, client):
        error_msg = "All fields (username, email, password) required"
        
        # Missing username
        response = register_user(client, None, "validemail@example.com", "validpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == error_msg

        # Missing email
        response = register_user(client, "validusername", None, "validpassword123")
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == error_msg

        # Missing password
        response = register_user(client, "validusername", "validemail@example.com", None)
        assert response.status_code == 400
        response_data = response.get_json()
        assert response_data["msg"] == error_msg


# TC-14: Login user

@allure.parent_suite("Authentication tests")
@allure.suite("TC-14: Login user")
@allure.severity(allure.severity_level.CRITICAL)
class TestLoginUser:

    @allure.sub_suite("Login with valid credentials")
    @allure.description("Test logging in with valid username and password. Verify that access and refresh tokens are returned.")
    def test_login_with_valid_credentials(self, client, mock_db):
        db = mock_db

        username = "testuser"
        password = "validpassword123"
        passwordhash = generate_password_hash(password)

        db["users"].insert_one({
            "username": username,
            "email": "testuser@example.com",
            "password": passwordhash
        })

        response = login_user(client, username, password)
        assert response.status_code == 200
        
        response_data = response.get_json()
        assert "access_token" in response_data
        assert "refresh_token" in response_data


    @allure.sub_suite("Login with invalid credentials")
    @allure.description("Test logging in with invalid username or password. Verify that appropriate error messages are returned.")
    def test_login_with_invalid_credentials(self, client, mock_db):
        db = mock_db

        username = "testuser"
        correct_password = "validpassword123"
        passwordhash = generate_password_hash(correct_password)

        db["users"].insert_one({
            "username": username,
            "email": "testuser@example.com",
            "password": passwordhash
        })

        # Invalid username
        response = login_user(client, "wronguser", correct_password)
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data["msg"] == "Wrong username or password"

        # Invalid password
        response = login_user(client, username, "wrongpassword")
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data["msg"] == "Wrong username or password"


    @allure.sub_suite("Login with nonexistent user")
    @allure.description("Test logging in with a username that does not exist in the database. Verify that appropriate error message is returned.")
    def test_login_with_nonexistent_user(self, client):
        response = login_user(client, "nonexistentuser", "password")
        assert response.status_code == 401
        response_data = response.get_json()
        assert response_data["msg"] == "Wrong username or password"