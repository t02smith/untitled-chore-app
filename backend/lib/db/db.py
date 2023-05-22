from azure.cosmos.aio import CosmosClient
from azure.cosmos.aio._database import DatabaseProxy
from azure.cosmos.aio._container import ContainerProxy
from config import config
from azure.cosmos import exceptions, PartitionKey
from fastapi import Depends


def get_client() -> CosmosClient:
    return CosmosClient(config["resource_uri"], credential=config["primary_key"])


async def get_or_create_database(
    client: CosmosClient, database: str = config["database"]
) -> DatabaseProxy:
    try:
        db = client.get_database_client(database)
        await db.read()
        return db
    except exceptions.CosmosResourceNotFoundError:
        return await client.create_database(database)


async def get_or_create_container(
    client: CosmosClient,
    container: str,
    db: str = config["database"],
    partition_key: str = "/id",
) -> ContainerProxy:

    try:
        db_obj = await get_or_create_database(client, db)
        container_obj = db_obj.get_container_client(container)
        await container_obj.read()
        return container_obj
    except exceptions.CosmosResourceNotFoundError:
        return await db_obj.create_container(
            id=container, partition_key=PartitionKey(partition_key)
        )
    except exceptions.CosmosHttpResponseError as e:
        raise e
