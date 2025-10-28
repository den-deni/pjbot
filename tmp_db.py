import aiosqlite



class Database:
    def __init__(self, db='data.db'):
        self.db = db





    async def create_table(self):
        async with aiosqlite.connect(self.db) as database:
            await database.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    tg_id INTEGER PRIMARY KEY,
                    username TEXT  NOT NULL,
                    key BLOB,
                    status BOOLEAN DEFAULT FALSE
                )
            ''')
            await database.commit()




    async def create_user(self, tg_id: int, username: str, status: bool = 0):
        """Створити користувача, якщо ще не існує"""
        async with aiosqlite.connect(self.db) as  database:
            async with database.execute("SELECT * FROM user WHERE tg_id =?", (tg_id,)) as cursor:
                result = await cursor.fetchone()
                if not result:
                    await database.execute("INSERT INTO user (tg_id, username, status) VALUES (?, ?, ?)", (tg_id, username, status))
                    await database.commit()

 
 
 
    async def user_exists(self, tg_id: int) -> bool:
        """Перевірити чи існує користувач"""
        async with aiosqlite.connect(self.db) as database:
            async with database.execute("SELECT 1 FROM user WHERE tg_id = ?", (tg_id, )) as cursor:
                return await cursor.fetchone() is not None
            



    async def get_key(self, tg_id: int):
        """Отримати ключ користувача"""
        async with aiosqlite.connect(self.db) as database:
            async with database.execute("SELECT key FROM user WHERE tg_id = ?", (tg_id, )) as cursor:
                key = await cursor.fetchone()
            return key[0] if key else None






    async def set_key(self, tg_id: int, key: bytes):
        """Записати ключ"""
        async with aiosqlite.connect(self.db) as database:
            await database.execute("UPDATE user SET key = ? WHERE tg_id = ?", (key, tg_id))
            await database.commit()




    async def update_key(self, tg_id: int, new_key: bytes):
        """Оновити ключ"""
        async with aiosqlite.connect(self.db) as database:
            await database.execute("UPDATE user SET key = ? WHERE tg_id = ?", (new_key, tg_id))
            await database.commit()




    async def delete_key(self, tg_id: int):
        """Видалити ключ"""
        async with aiosqlite.connect(self.db) as database:
            await database.execute("UPDATE user SET key = NULL WHERE tg_id = ?", (tg_id, ))
            await database.commit()




    async def get_status(self, tg_id: int) -> bool:
        """Отримати статус користувача"""
        async with aiosqlite.connect(self.db) as database:
            async with database.execute("SELECT status FROM user WHERE tg_id = ?", (tg_id, )) as cursor:
                status = await cursor.fetchone()
            return bool(status[0]) if status else False
        



    async def set_status(self, tg_id: int, status: bool):
        """Змінити статус користувача"""
        async with aiosqlite.connect(self.db) as databese:
            await databese.execute("UPDATE user SET status = ? WHERE tg_id = ?", (status, tg_id))
            await databese.commit()
