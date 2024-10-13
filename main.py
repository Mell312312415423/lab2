from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

application = FastAPI()

task_storage = [
    {"id": 1, "title": "Homework", "description": "Finish math problems", "completed": False}
]

class Item(BaseModel):
    title: str = Field(..., min_length=1, description="The task's title")
    description: Optional[str] = Field(None, description="Details about the task")
    completed: bool = False

class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, description="The task's title")
    description: Optional[str] = Field(None, description="Details about the task")
    completed: Optional[bool] = None

def search_task(task_id: int):
    for task in task_storage:
        if task["id"] == task_id:
            return task
    return None

@application.get("/items/{task_id}")
def fetch_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Task ID must be a positive integer"})
    
    task = search_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": f"Task with ID {task_id} not found"})
    
    return {"status": "success", "data": task}

@application.post("/items")
def add_task(item: Item):
    new_task_id = len(task_storage) + 1
    new_item = {
        "id": new_task_id,
        "title": item.title,
        "description": item.description,
        "completed": item.completed
    }
    task_storage.append(new_item)
    
    return {"status": "success", "data": new_item}

@application.patch("/items/{task_id}")
def modify_task(task_id: int, item_update: ItemUpdate):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Task ID must be a positive integer"})
    
    task = search_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": f"Task with ID {task_id} not found"})
    
    if item_update.title is not None:
        task["title"] = item_update.title
    if item_update.description is not None:
        task["description"] = item_update.description
    if item_update.completed is not None:
        task["completed"] = item_update.completed
    
    return {"status": "success", "data": task}

@application.delete("/items/{task_id}")
def remove_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Task ID must be a positive integer"})
    
    task = search_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": f"Task with ID {task_id} not found"})
    
    task_storage.remove(task)
    return {"status": "success", "message": f"Task with ID {task_id} was deleted"}

@application.put("/items/{task_id}")
def replace_task(task_id: int, item: Item):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail={"error": "Task ID must be a positive integer"})

    task = search_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"error": f"Task with ID {task_id} not found"})
    
    task["title"] = item.title
    task["description"] = item.description
    task["completed"] = item.completed
    
    return {"status": "success", "data": task}