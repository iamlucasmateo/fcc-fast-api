from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Iterable, Tuple

from pydantic import BaseModel
import psycopg2

from src.utils.config import ConfigParser
from src.schemas import PostBase, PostCreate
from src.repository.general import Repository
from src.utils.config import ConfigParser

class PostRepository(Repository):
    @abstractmethod
    def create(self, payload: PostCreate):
        pass

    @abstractmethod
    def read_all(self):
        pass
    
    @abstractmethod
    def read_one(self, id: int):
        pass

    @abstractmethod
    def update(self, id: int, payload: PostCreate):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass


class InMemoryPostRepository(PostRepository):
    init_data = {
        1: PostBase(
            title="My post", 
            content="Writing something",
            published=False
        ),
        2: PostBase(
            title = "Pizza",
            content = "I love pizza",
        ),
        3: PostBase(
            title = "Politics",
            content = "Sharing my opinion",
        )
    }
    
    def __init__(self, data: Dict[int, PostCreate] = init_data) -> None:
        self.data = data

    def create(self, payload: PostCreate) -> PostCreate:
        new_index = max(self.data.keys()) + 1
        self.data[new_index] = payload
        return payload
    
    def read_all(self):
        return self.data

    def read_one(self, id: int):
        result = self.data.get(id, None)
        return result

    def delete(self, id: int):
        deleted = self.data.pop(id)
        return deleted
    
    def update(self, id: int, payload: PostCreate):
        if id not in self.data.keys():
            raise KeyError(f"id {id} does not exist in this database")
        # TODO: this should check if all keys are indicated in payload
        new_values = self.data[id].dict()
        new_values.update(payload.dict())
        self.data[id] = PostCreate(**new_values)
        return payload


class PostSQLQueries:
    def __init__(self, config: Optional[Dict[str, str]] = None):
        if not config:
            config = ConfigParser()
            env = config.get_env()
            config = config.get_data(paths=["DATABASE", env])
        self.config = config
        self.schema = self.config['OTHER']['schema']
    
    def get_cols(self):
        return f"SELECT column_name FROM information_schema.columns " + \
                f"WHERE table_schema = '{self.schema}' AND table_name = 'posts';"
    
    def read_all(self):
        return f"SELECT * FROM {self.schema}.posts;"
    
    def read_one(self):
        return f"SELECT * FROM {self.schema}.posts WHERE id = %s;"
    
    def create(self, payload: dict):
        placeholder = self.arr2string([f'%({col})s' for col in payload.keys()], 
                                      init='(', end=')',
                                      before='', after=', ')
        placeholder = placeholder[:-3] + ')'
        cols = self.arr2string(payload.keys(),
                               init='(', end=')',
                               before='', after=', ')
        cols = cols[:-3] + ')'
        query = f"INSERT INTO {self.schema}.posts {cols} VALUES {placeholder}"
        return query
    
    def update(self, payload: dict):
        cols_for_update_query = [f'{col} = %s' for col in payload.keys()]
        placeholder = self.arr2string(cols_for_update_query, after=', ')
        placeholder = placeholder[:-2]
        query = f"UPDATE {self.schema}.posts SET {placeholder} WHERE id = %s"
        return query
    
    def delete(self):
        return f"DELETE FROM {self.schema}.posts WHERE id = %s RETURNING *"

    
    @staticmethod
    def arr2string(arr: List[str], 
                   before: str = '',
                   after: str = '',
                   init: str = '',
                   end: str = ''):
        result = init
        for item in arr:
            result += before + item + after
        result += end
        return result


class PostgresPostSQLQueries(PostSQLQueries):
    pass


class SQLPostRepository(PostRepository):
    def __init__(self, 
                 connection_data: Dict[str, str],
                 connection_handler: Any,
                 queries: PostSQLQueries,
                 cols: Optional[List[str]] = None):
        self.connection_handler = connection_handler
        self.connection = self.connection_handler.connect(**connection_data)
        self.cursor = self.connection.cursor()
        self.queries = queries
        self.cols = cols
        if not cols:
            cols_query = self.queries.get_cols()
            self.cursor.execute(cols_query)
            # formatting result as list
            self.cols = [item[0] for item in self.cursor.fetchall()]


class PostgreSQLPostRepository(SQLPostRepository):
    def read_one(self, id: int):
        """Returns post with the indicated id"""
        query = self.queries.read_one()
        self.cursor.execute(query, (id,))
        values = self.cursor.fetchone()
        if not values:
            return None
        post_data = self.values2post(values)
        post = PostBase(**post_data)
        return post
    
    def values2post(self, values: Iterable[Any]):
        """Receives all values as iterable, returns data for creating Post"""
        post_data = { col: value for col, value in zip(self.cols, values) }
        return post_data
    
    def read_all(self):
        """Returns all posts"""
        query = self.queries.read_all()
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        posts = (self.values2post(values) for values in data)
        return posts

    def update(self, id: int, payload: PostCreate):
        query = self.queries.update(payload.dict())
        values = tuple(list(payload.dict().values()) + [id])
        updated = self.cursor.execute(query, values)
        self.connection.commit()
        return updated
    
    def create(self, payload: PostCreate):
        """Creates post entry in Postgres DB"""
        query = self.queries.create(payload.dict())
        query_values = payload.dict()
        try:
            self.cursor.execute(query, query_values)
            self.connection.commit()
        except Exception as e:
            print(e)
    
    def delete(self, id: int):
        query = self.queries.delete()
        self.cursor.execute(query, (id,))
        deleted_value = self.cursor.fetchone()
        self.connection.commit()
        return deleted_value


# # connection
# config = ConfigParser()
# env = config.get_env()
# connection_data = config.get_data(paths=["DATABASE", env])
# conn = psycopg2.connect(**connection_data)

# # retrieval
# try:
#     cursor = conn.cursor()
#     query = "SELECT * FROM main.posts;"
#     cursor.execute(query)
#     data = cursor.fetchall()
#     print(data)
# except:
#     conn.rollback()

# # cleanup
# cursor.close()
# conn.commit()
# conn.close()




