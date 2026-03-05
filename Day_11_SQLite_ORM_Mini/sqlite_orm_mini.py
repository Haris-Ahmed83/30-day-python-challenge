
import sqlite3

class Field:
    def __init__(self, field_type, primary_key=False, default=None):
        self.field_type = field_type
        self.primary_key = primary_key
        self.default = default

    def __repr__(self):
        return f"<Field: {self.field_type}, PK: {self.primary_key}, Default: {self.default}>"

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)

        fields = {}
        table_name = attrs.get('table_name', name.lower() + 's')
        
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
        
        attrs['_fields'] = fields
        attrs['_table_name'] = table_name
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    _db_path = 'database.db'

    def __init__(self, **kwargs):
        for field_name, field_obj in self._fields.items():
            setattr(self, field_name, kwargs.get(field_name, field_obj.default))
        self.id = kwargs.get('id') # Assuming 'id' is always the primary key for simplicity

    @classmethod
    def _get_connection(cls):
        return sqlite3.connect(cls._db_path)

    @classmethod
    def create_table(cls):
        columns = []
        pk_field = None
        for field_name, field_obj in cls._fields.items():
            col_def = f"{field_name} {field_obj.field_type}"
            if field_obj.primary_key:
                col_def += " PRIMARY KEY AUTOINCREMENT"
                pk_field = field_name
            elif field_obj.default is not None:
                if isinstance(field_obj.default, str):
                    col_def += f" DEFAULT '{field_obj.default}'"
                else:
                    col_def += f" DEFAULT {field_obj.default}"
            columns.append(col_def)
        
        if not pk_field:
            columns.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")

        columns_str = ", ".join(columns)
        query = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({columns_str})"
        
        with cls._get_connection() as conn:
            conn.execute(query)
            conn.commit()

    def save(self):
        fields = []
        placeholders = []
        values = []
        
        for field_name, field_obj in self._fields.items():
            value = getattr(self, field_name)
            if value is not None and not field_obj.primary_key:
                fields.append(field_name)
                placeholders.append('?')
                values.append(value)

        if self.id:
            # Update existing record
            set_clauses = [f"{field} = ?" for field in fields]
            query = f"UPDATE {self._table_name} SET {', '.join(set_clauses)} WHERE id = ?"
            values.append(self.id)
            with self._get_connection() as conn:
                conn.execute(query, tuple(values))
                conn.commit()
        else:
            # Insert new record
            query = f"INSERT INTO {self._table_name} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            with self._get_connection() as conn:
                cursor = conn.execute(query, tuple(values))
                self.id = cursor.lastrowid
                conn.commit()
        return self

    def delete(self):
        if self.id:
            query = f"DELETE FROM {self._table_name} WHERE id = ?"
            with self._get_connection() as conn:
                conn.execute(query, (self.id,))
                conn.commit()
                self.id = None

    @classmethod
    def all(cls):
        query = f"SELECT id, {', '.join(cls._fields.keys())} FROM {cls._table_name}"
        with cls._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query)
            return [cls(id=row['id'], **{k: row[k] for k in cls._fields.keys()}) for row in cursor.fetchall()]

    @classmethod
    def get(cls, id):
        query = f"SELECT id, {', '.join(cls._fields.keys())} FROM {cls._table_name} WHERE id = ?"
        with cls._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, (id,))
            row = cursor.fetchone()
            if row:
                return cls(id=row['id'], **{k: row[k] for k in cls._fields.keys()})
            return None

    @classmethod
    def filter(cls, **kwargs):
        conditions = []
        values = []
        for k, v in kwargs.items():
            if k in cls._fields:
                conditions.append(f"{k} = ?")
                values.append(v)
        
        if not conditions:
            return cls.all()

        query = f"SELECT id, {', '.join(cls._fields.keys())} FROM {cls._table_name} WHERE {' AND '.join(conditions)}"
        with cls._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, tuple(values))
            return [cls(id=row['id'], **{k: row[k] for k in cls._fields.keys()}) for row in cursor.fetchall()]

    def __repr__(self):
        attrs = ', '.join(f"{k}={getattr(self, k)!r}" for k in self._fields.keys())
        return f"<{self.__class__.__name__} id={self.id}, {attrs}>"

# Example Usage:
if __name__ == "__main__":
    class User(Model):
        table_name = 'users'
        name = Field('TEXT')
        email = Field('TEXT', primary_key=False, default='no_email@example.com')
        age = Field('INTEGER', default=18)

    class Product(Model):
        name = Field('TEXT')
        price = Field('REAL')

    # Set the database path (optional, defaults to database.db)
    Model._db_path = 'my_app.db'

    # Create tables
    User.create_table()
    Product.create_table()

    # Create users
    user1 = User(name='Alice', email='alice@example.com')
    user1.save()
    print(f"Created user: {user1}")

    user2 = User(name='Bob') # Using default email and age
    user2.save()
    print(f"Created user: {user2}")

    # Update user
    user1.age = 30
    user1.save()
    print(f"Updated user: {user1}")

    # Get all users
    all_users = User.all()
    print("\nAll users:")
    for user in all_users:
        print(user)

    # Get user by ID
    fetched_user = User.get(user2.id)
    print(f"\nFetched user by ID {user2.id}: {fetched_user}")

    # Filter users
    filtered_users = User.filter(name='Alice')
    print("\nFiltered users by name 'Alice':")
    for user in filtered_users:
        print(user)

    # Create products
    product1 = Product(name='Laptop', price=1200.50)
    product1.save()
    print(f"\nCreated product: {product1}")

    product2 = Product(name='Mouse', price=25.00)
    product2.save()
    print(f"Created product: {product2}")

    # Delete user
    user2.delete()
    print(f"\nDeleted user: {user2.name}")

    # Verify deletion
    remaining_users = User.all()
    print("Remaining users after deletion:")
    for user in remaining_users:
        print(user)

    # Clean up the database file for example run
    import os
    if os.path.exists(Model._db_path):
        os.remove(Model._db_path)
        print(f"\nCleaned up database file: {Model._db_path}")
