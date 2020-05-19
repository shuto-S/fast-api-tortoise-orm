from typing import List
from fastapi import APIRouter, Depends
from starlette.status import HTTP_204_NO_CONTENT

from app.services.auth import get_current_user
from app.services.exceptions import HTTP_404_NOT_FOUND
from app.models.todo import Todo_Pydantic, TodoIn_Pydantic, Todo
from app.models.user import User


tags = ["todos"]
router = APIRouter()


@router.post("/todos", tags=tags, response_model=Todo_Pydantic)
async def create(form_data: TodoIn_Pydantic, user: User = Depends(get_current_user)):
    todo = await Todo.create(**form_data.dict(exclude_unset=True), user=user)
    return await Todo_Pydantic.from_tortoise_orm(todo)


@router.get("/todos", tags=tags, response_model=List[Todo_Pydantic])
async def get_list(user: User = Depends(get_current_user)):
    return await Todo_Pydantic.from_queryset(Todo.filter(user=user))


@router.get("/todos/{todo_id}", tags=tags, response_model=Todo_Pydantic)
async def get_detail(todo_id: int, user: User = Depends(get_current_user)):
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        raise HTTP_404_NOT_FOUND
    return todo


@router.patch("/todos/{todo_id}", tags=tags, response_model=Todo_Pydantic)
async def update(todo_id: int, form_data: TodoIn_Pydantic, user: User = Depends(get_current_user)):
    todo = await Todo.get_or_none(id=todo_id, user=user)
    if not todo:
        raise HTTP_404_NOT_FOUND
    await todo.update_from_dict(form_data.dict(exclude_unset=True)).save()
    return await Todo_Pydantic.from_tortoise_orm(todo)


@router.delete("/todos/{todo_id}", tags=tags, status_code=HTTP_204_NO_CONTENT)
async def delete(todo_id: int, user: User = Depends(get_current_user)):
    deleted_count = await Todo.filter(id=todo_id, user=user).delete()
    if not deleted_count:
        raise HTTP_404_NOT_FOUND
