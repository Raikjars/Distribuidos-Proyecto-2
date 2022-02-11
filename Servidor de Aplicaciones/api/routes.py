from typing import  List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from model.object_model import ObjectInJson
from repository.repo_object import ObjectRepo

router = APIRouter()

@router.post("/create", response_model=ObjectInJson, status_code=status.HTTP_201_CREATED)
def create_object(new_object: ObjectInJson = Body(..., embed=True)):
    object_repo = ObjectRepo()
    
    return object_repo.create(new_object=new_object)

@router.delete("/delete/{id}/")
def delete_one_object(id: int) -> int:
    object_repo = ObjectRepo()
    delete_id =  object_repo.delete(id=id)

    if not delete_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {"delete_id" : delete_id}

@router.get("/", response_model=List[ObjectInJson], status_code=status.HTTP_200_OK)
def get_all_object():
    object_repo = ObjectRepo()
    return object_repo.get_all()

@router.get("/{id}/", response_model=List[ObjectInJson], status_code=status.HTTP_200_OK)
def get_one_object(id: int):
    object_repo = ObjectRepo()
    objectData =  object_repo.get_by_id(id=id)

    if not objectData:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return objectData

@router.post("/replicate", response_model=ObjectInJson, status_code=status.HTTP_201_CREATED)
def replicate_object(new_object: ObjectInJson = Body(..., embed=True)):
    object_repo = ObjectRepo()
    
    return object_repo.replicate(new_object=new_object)

@router.get("/restore", response_model=List[ObjectInJson], status_code=status.HTTP_200_OK)
def restore_object():
    object_repo = ObjectRepo()
    return object_repo.restore()