import asyncio
import aiohttp
import logging
from rest_framework import status
from pydantic import ValidationError
from app1.models import Model

logger = logging.getLogger(__name__)

async def parse_data(article, is_file=False):
    url = f"https://wbx-content-v2.wbstatic.net/ru/{article}.json"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == status.HTTP_200_OK:
                    result = await response.json()

                    try:
                        item_info = Model.parse_obj(result)
                        return item_info.dict()
                    except ValidationError as err:
                        logger.error(f"Error - {err}.")

                elif response.status == status.HTTP_204_NO_CONTENT:
                    if not is_file:
                        logger.info(f"Article {article} not found")
                    else:
                        item_info = Model(nm_id=article)
                        return item_info.dict()
                else:
                    logger.info(f"Response from url has status: {response.status}")
        except aiohttp.ClientError as err:
            logger.error(f"Error with connection to url: {err}")


def task_run(articles):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = []
    for article in articles:
        task = parse_data(article, is_file=True)
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    return result


def task_one_run(article):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(parse_data(article))
    return result
