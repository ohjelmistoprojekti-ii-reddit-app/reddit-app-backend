import allure
import pytest
from app.services.db import save_data_to_database, fetch_data_from_collection, update_one_item_in_collection, delete_one_item_from_collection


# TC-01: Save data to database

@allure.parent_suite("Database tests")
@allure.suite("TC-01: Save data to database")
@allure.severity(allure.severity_level.CRITICAL)
class TestSaveDataToDatabase:
    
    @allure.sub_suite("Save one item")
    @allure.description("Test saving a single document to the database, and verify it was saved correctly.")
    def test_save_one_document(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"

        save_data_to_database(test_data, collection)
        saved_data = list(db[collection].find({}))

        assert len(saved_data) == 1
        assert saved_data[0]["title"] == "Test Post"
        assert saved_data[0]["content"] == "This is a test post"


    @allure.sub_suite("Save list of items")
    @allure.description("Test saving multiple documents to the database, and verify they were saved correctly.")
    def test_save_multiple_documents(self, mock_db):
        db = mock_db

        test_data = [
            { "title": "Test Post", "content": "This is a test post" },
            { "title": "Another Post", "content": "This is another post"}
        ]
        collection = "test_collection"

        save_data_to_database(test_data, collection)
        saved_data = list(db[collection].find({}))

        assert len(saved_data) == 2
        assert saved_data[0]["title"] == "Test Post"
        assert saved_data[1]["title"] == "Another Post"


    @allure.sub_suite("Save empty list")
    @allure.description("Test saving an empty list to the database, and verify that a ValueError is raised.")
    def test_save_empty_list(self, mock_db):
        test_data = []
        collection = "test_collection"

        with pytest.raises(ValueError):
            save_data_to_database(test_data, collection)


    @allure.sub_suite("Save invalid data type")
    @allure.description("Test saving an invalid data type to the database, and verify that a TypeError is raised.")
    def test_save_invalid_data_type(self, mock_db):
        test_data = "This is a string"
        collection = "test_collection"

        with pytest.raises(TypeError):
            save_data_to_database(test_data, collection)


# TC-02: Fetch data from database

@allure.parent_suite("Database tests")
@allure.suite("TC-02: Fetch data from database")
@allure.severity(allure.severity_level.CRITICAL)
class TestFetchDataFromDatabase:
    
    @allure.sub_suite("Fetch all documents")
    @allure.description("Test fetching all documents from the database collection, and verify that the correct documents are returned as a list.")
    def test_fetch_all_documents(self, mock_db):
        db = mock_db

        test_data = [
            { "title": "Test Post", "content": "This is a test post" },
            { "title": "Another Post", "content": "This is another post"}
        ]
        collection = "test_collection"

        db[collection].insert_many(test_data)
        fetched_data = fetch_data_from_collection(collection)

        assert isinstance(fetched_data, list)
        assert len(fetched_data) == 2
        assert fetched_data[0]["title"] == "Test Post"
        assert fetched_data[1]["title"] == "Another Post"


    @allure.sub_suite("Fetch documents with filter")
    @allure.description("Test fetching documents with a filter, and verify that the correct documents are returned as a list.")
    def test_fetch_documents_using_filter(self, mock_db):
        db = mock_db

        test_data = [
            { "title": "Test Post", "content": "This is a test post" },
            { "title": "Another Post", "content": "This is another post"}
        ]
        collection = "test_collection"

        db[collection].insert_many(test_data)
        fetched_data = fetch_data_from_collection(collection, filter={"title": "Another Post"})

        assert len(fetched_data) == 1
        assert isinstance(fetched_data, list)
        assert fetched_data[0]["title"] == "Another Post"


    @allure.sub_suite("Fetch non-existent document")
    @allure.description("Test fetching a document that doesn't exist, and verify that an empty list is returned.")
    def test_fetch_nonexistent_document(self, mock_db):
        db = mock_db

        test_data = [
            { "title": "Test Post", "content": "This is a test post" },
            { "title": "Another Post", "content": "This is another post"}
        ]
        collection = "test_collection"

        db[collection].insert_many(test_data)
        fetched_data = fetch_data_from_collection(collection, filter={"title": "Nonexistent"})

        assert len(fetched_data) == 0
        assert isinstance(fetched_data, list)


    @allure.sub_suite("Fetch with invalid filter")
    @allure.description("Test fetching documents with invalid filter, and verify that a TypeError is raised.")
    def test_fetch_documents_with_invalid_filter_type(self, mock_db):
        collection = "test_collection"

        with pytest.raises(TypeError):
            fetch_data_from_collection(collection, filter="Invalid filter")


# TC-03: Update data in database

@allure.parent_suite("Database tests")
@allure.suite("TC-03: Update data in database")
@allure.severity(allure.severity_level.CRITICAL)
class TestUpdateDataInDatabase:
    
    @allure.sub_suite("Update existing document")
    @allure.description("Test updating existing document, and verify it was updated successfully.")
    def test_update_existing_document(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"

        db[collection].insert_one(test_data)
        update_one_item_in_collection(collection, {"title": "Test Post"}, {"$set": {"content": "Updated content"}})
        
        updated_item = db[collection].find_one({"title": "Test Post"})
        assert updated_item["content"] == "Updated content"


    @allure.sub_suite("Update non-existent document")
    @allure.description("Test updating non-existing document, and verify that a ValueError was raised.")
    def test_update_nonexisting_document(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"
        db[collection].insert_one(test_data)

        with pytest.raises(ValueError):
            update_one_item_in_collection(collection, {"title": "Nonexistent"}, {"$set": {"content": "Updated content"}})


    @allure.sub_suite("Update with invalid filter")
    @allure.description("Test updating using an invalid filter, and verify that a TypeError was raised.")
    def test_update_with_invalid_filter_type(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"
        db[collection].insert_one(test_data)

        with pytest.raises(TypeError):
            update_one_item_in_collection(collection, "Invalid filter", {"$set": {"content": "Updated content"}})


# TC-04: Delete data from database

@allure.parent_suite("Database tests")
@allure.suite("TC-04: Delete data from database")
@allure.severity(allure.severity_level.CRITICAL)
class TestDeleteDataFromDatabase:
    
    @allure.sub_suite("Delete existing document")
    @allure.description("Test deleting existing document, and verify it was deleted successfully.")
    def test_delete_existing_document(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"
        db[collection].insert_one(test_data)

        result = delete_one_item_from_collection(collection, {"title": "Test Post"})
        
        # Function should return 1 for one deleted document
        assert result == 1

        deleted_item = db[collection].find_one({"title": "Test Post"})
        assert deleted_item is None


    @allure.sub_suite("Delete non-existing document")
    @allure.description("Test deleting non-existing document, and verify it is handled gracefully.")
    def test_delete_nonexisting_document(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"
        db[collection].insert_one(test_data)

        result = delete_one_item_from_collection(collection, {"title": "Nonexistent"})
        assert result == 0 # Expecting 0 deleted documents


    @allure.sub_suite("Delete with invalid filter")
    @allure.description("Test deleting with invalid filter, and verify that a TypeError was raised.")
    def test_delete_with_invalid_filter_type(self, mock_db):
        db = mock_db

        test_data = { "title": "Test Post", "content": "This is a test post" }
        collection = "test_collection"
        db[collection].insert_one(test_data)

        with pytest.raises(TypeError):
            delete_one_item_from_collection(collection, "Test Post")






