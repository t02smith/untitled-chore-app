from lib.db import user, home as db, types
from fastapi import HTTPException

async def get_leaderboard(players: list[types.User]) -> list[types.User]:
  async with db.get_client() as client:
    container = await db.get_or_create_container(client, "leaderboard")
    return [types.User(**u) async for u in container.query_items(
      """
      SELECT *
      FROM users u
      ORDER BY u.score DESC,
      """, #parameters=[{"name": "@n", "value": players}]
    )]