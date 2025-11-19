import allure
import pytest
from app.services.db import save_data_to_database

@allure.epic("Database tests")
@allure.suite("TC-01: Save data to database")
@allure.sub_suite("Save one item")
@allure.description("Test saving a single document to the database, and verify it was saved correctly.")
@allure.severity(allure.severity_level.CRITICAL)
def test_save_one_document(mock_db):
    client, db = mock_db

    test_data = { "title": "Test Post", "content": "This is a test post" }
    collection = "test_collection"

    save_data_to_database(test_data, collection)
    saved_data = list(db[collection].find({}))
    assert len(saved_data) == 1
    assert saved_data[0]["title"] == "Test Post"
    assert saved_data[0]["content"] == "This is a test post"


@allure.epic("Database tests")
@allure.suite("TC-01: Save data to database")
@allure.sub_suite("Save list of items")
@allure.description("Test saving multiple documents to the database, and verify they were saved correctly.")
@allure.severity(allure.severity_level.CRITICAL)
def test_save_multiple_documents(mock_db):
    client, db = mock_db

    test_data = [
        { "title": "Test Post", "content": "This is a test post" },
        { "title": "Another Post", "content": "This is a another post"}
    ]
    collection = "test_collection"

    save_data_to_database(test_data, collection)
    saved_data = list(db[collection].find({}))
    assert len(saved_data) == 2
    assert saved_data[0]["title"] == "Test Post"
    assert saved_data[1]["title"] == "Another Post"


@allure.epic("Database tests")
@allure.suite("TC-01: Save data to database")
@allure.sub_suite("Save empty list")
@allure.description("Test saving an empty list to the database, and verify that a ValueError is raised.")
@allure.severity(allure.severity_level.CRITICAL)
def test_save_empty_list(mock_db):
    client, db = mock_db

    test_data = []
    collection = "test_collection"
    with pytest.raises(ValueError):
        save_data_to_database(test_data, collection)


@allure.epic("Database tests")
@allure.suite("TC-01: Save data to database")
@allure.sub_suite("Save invalid data type")
@allure.description("Test saving an invalid data type to the database, and verify that a TypeError is raised.")
@allure.severity(allure.severity_level.CRITICAL)
def test_save_invalid_data_type(mock_db):
    client, db = mock_db

    test_data = "This is a string"
    collection = "test_collection"
    with pytest.raises(TypeError):
        save_data_to_database(test_data, collection)