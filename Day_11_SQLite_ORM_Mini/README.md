# Day 11 — SQLite ORM Mini

This project implements a lightweight Object-Relational Mapper (ORM) on top of `sqlite3` for Python. It provides a simple way to interact with SQLite databases using Python classes and objects, abstracting away raw SQL queries.

## Features

-   **Model Definition**: Define database tables as Python classes with fields representing columns.
-   **Field Types**: Basic support for `TEXT`, `INTEGER`, `REAL` field types.
-   **Primary Keys**: Automatic handling of `id` as a primary key with `AUTOINCREMENT`.
-   **Default Values**: Specify default values for fields.
-   **Table Creation**: Automatically create tables based on model definitions.
-   **CRUD Operations**: 
    -   `save()`: Insert new records or update existing ones.
    -   `delete()`: Remove records from the database.
    -   `all()`: Retrieve all records for a model.
    -   `get(id)`: Retrieve a single record by its primary key.
    -   `filter(**kwargs)`: Filter records based on field values.

## How to Use

1.  **Define your Models**: Create Python classes that inherit from `Model` and define your fields using the `Field` class.

    ```python
    from sqlite_orm_mini import Model, Field

    class User(Model):
        table_name = 'users' # Optional: defaults to class name + s (e.g., users)
        name = Field('TEXT')
        email = Field('TEXT', default='no_email@example.com')
        age = Field('INTEGER', default=18)
    ```

2.  **Set Database Path**: (Optional) You can set the database file path by modifying `Model._db_path`.

    ```python
    Model._db_path = 'my_application.db'
    ```

3.  **Create Tables**: Call the `create_table()` class method for each of your models.

    ```python
    User.create_table()
    ```

4.  **Perform CRUD Operations**:

    -   **Create/Update**:

        ```python
        user1 = User(name='Alice', email='alice@example.com')
        user1.save() # Inserts a new record

        user1.age = 30
        user1.save() # Updates the existing record
        ```

    -   **Retrieve All**:

        ```python
        all_users = User.all()
        for user in all_users:
            print(user.name, user.email, user.age)
        ```

    -   **Retrieve by ID**:

        ```python
        fetched_user = User.get(user1.id)
        print(fetched_user.name)
        ```

    -   **Filter**:

        ```python
        filtered_users = User.filter(name='Alice')
        for user in filtered_users:
            print(user.email)
        ```

    -   **Delete**:

        ```python
        user1.delete()
        ```

## Project Structure

```
Day_11_SQLite_ORM_Mini/
├── sqlite_orm_mini.py    # The ORM implementation and example usage
└── README.md             # Project description and usage instructions
```

## Example Usage (from `sqlite_orm_mini.py`)

The `if __name__ == "__main__":` block in `sqlite_orm_mini.py` demonstrates how to use the ORM with `User` and `Product` models, covering table creation, record insertion, updates, retrieval, filtering, and deletion. Running the script will execute these examples and print the results to the console.
