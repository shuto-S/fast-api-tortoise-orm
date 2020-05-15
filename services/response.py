from tortoise.contrib.fastapi import HTTPNotFoundError


HTTP_404_NOT_FOUND = {404: {"model": HTTPNotFoundError}}
