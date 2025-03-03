import pytest

from asyncmy.cursors import DictCursor


@pytest.mark.asyncio
async def test_fetchone(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT 1")
        ret = await cursor.fetchone()
        assert ret == (1,)


@pytest.mark.asyncio
async def test_fetchall(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("SELECT 1")
        ret = await cursor.fetchall()
        assert ret == ((1,),)


@pytest.mark.asyncio
async def test_dict_cursor(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        await cursor.execute("SELECT 1")
        ret = await cursor.fetchall()
        assert ret == [{"1": 1}]


@pytest.mark.asyncio
async def test_insert(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        rows = await cursor.execute(
            """INSERT INTO test.asyncmy(id,`decimal`, date, datetime, `float`, string, `tinyint`) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (
                -1,
                1,
                "2020-08-08",
                "2020-08-08 00:00:00",
                1,
                "1",
                1,
            ),
        )
        assert rows == 1


@pytest.mark.asyncio
async def test_delete(connection):
    async with connection.cursor() as cursor:
        rows = await cursor.execute("delete from test.asyncmy where id = -1")
        assert rows == 0


@pytest.mark.asyncio
async def test_executemany(connection):
    async with connection.cursor(cursor=DictCursor) as cursor:
        rows = await cursor.executemany(
            """INSERT INTO test.asyncmy(`decimal`, date, datetime, `float`, string, `tinyint`) VALUES (%s,%s,%s,%s,%s,%s)""",
            [
                (
                    1,
                    "2020-08-08",
                    "2020-08-08 00:00:00",
                    1,
                    "1",
                    1,
                ),
                (
                    1,
                    "2020-08-08",
                    "2020-08-08 00:00:00",
                    1,
                    "1",
                    1,
                ),
            ],
        )
        assert rows == 2


@pytest.mark.asyncio
async def test_table_ddl(connection):
    async with connection.cursor() as cursor:
        await cursor.execute("drop table if exists test.alter_table")
        create_table_sql = """
            CREATE TABLE test.alter_table
(
    `id` int primary key auto_increment
)
            """
        await cursor.execute(create_table_sql)
        add_column_sql = "alter table test.alter_table add column c varchar(20)"
        await cursor.execute(add_column_sql)
        await cursor.execute("drop table test.alter_table")
