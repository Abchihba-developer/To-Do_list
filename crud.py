from sqlalchemy import text
from typing import List, Optional
from database import async_engine, async_session_factory
from models import Task_DB
from shemas import Task


async def create_db_table():
    async with async_engine.connect() as conn:
        await conn.run_sync(Task_DB.metadata.drop_all)
        await conn.run_sync(Task_DB.metadata.create_all)
        await conn.commit()

async def create_task(title: str, description: str | None = None, completed: bool | None = False):
    async with async_engine.connect() as conn:
        stmt = text("""INSERT INTO tasks (title, description, completed) 
        VALUES (:param1, :param2, :param3)""")
        await conn.execute(stmt, {"param1": title,
                                  "param2": description,
                                  "param3": completed})
        await conn.commit()

async def get_task(task_id: int) -> Task:
    async with async_engine.connect() as conn:
        stmt = text("SELECT * FROM tasks WHERE id=:param1")
        res = await conn.execute(stmt, {"param1": task_id})
        return res.fetchone()

async def get_tasks(skip: int = 0, limit: int = 10) -> List[Task]:
    async with async_engine.connect() as conn:
        stmt = text("""SELECT * FROM tasks 
        ORDER BY id 
        LIMIT :param1 OFFSET :param2""")
        res = await conn.execute(stmt, {"param1": limit, "param2": skip})
        return res.fetchall()

async def update_task(task_id: int, title: str | None = None, description: str | None = None, completed: bool | None = None):
    async with async_engine.connect() as conn:
        query = "UPDATE tasks SET"
        params = {}
        updates = []
        if title is not None:
            updates.append(" title = :param1")
            params["param1"] = title
        if description is not None:
            updates.append(" description = :param2")
            params["param2"] = description
        if completed is not None:
            updates.append(" completed = :param3")
            params["param3"] = completed
        if not updates:
            raise ValueError("Не указано ни одного поля для обновления")

        query += ",".join(updates) + " WHERE id = :param4"
        params["param4"] = task_id
        await conn.execute(text(query), params)
        await conn.commit()

async def delete_task(task_id: int):
    async with async_engine.connect() as conn:
        await conn.execute(text("DELETE FROM tasks WHERE id = :param1"), {"param1": task_id})
        await conn.commit()


