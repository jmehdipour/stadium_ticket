from fastapi import APIRouter, HTTPException, Depends
from mongoengine import NotUniqueError

from src.api.middlewares import is_admin
from src.api.schemas import StadiumIn
from src.data.connections.mongodb import counter
from src.data.models.mongodb import Stadium

router = APIRouter()


@router.get('/stadiums')
def get_all_stadiums(size: int = 10, last_id: int = None, first_id: int = None):
    if first_id and not last_id:
        stadiums = Stadium.objects(id__gt=first_id)
    elif not first_id and last_id:
        stadiums = Stadium.objects(id__lt=last_id)
    else:
        stadiums = Stadium.objects()

    stadium_dict_list = [stadium.to_mongo() for stadium in stadiums.order_by('-id').limit(size)]
    return stadium_dict_list


@router.post('/stadiums', dependencies=[Depends(is_admin)])
def create_stadium(stadium_data: StadiumIn):
    try:
        mongo_stadium = Stadium(id=counter('stadium'), **stadium_data.dict())
        mongo_stadium.save()
    except NotUniqueError as ex:
        raise HTTPException(status_code=409, detail="duplicate stadium name")
    except Exception as ex:
        raise HTTPException(status_code=500, detail="internal server error")
    return mongo_stadium.to_mongo()


@router.put('/stadiums/{stadium_id}', dependencies=[Depends(is_admin)])
def update_stadium(stadium_id: int, stadium_data: StadiumIn):
    try:
        Stadium.objects(id=stadium_id).update(**stadium_data.dict())
    except Exception as ex:
        raise HTTPException(status_code=500, detail="internal server error")
    return {'result': True}


@router.delete('/stadiums/{stadium_id}')
def delete_stadium(stadium_id: int):

    stadium = Stadium.objects(id=stadium_id).first()
    if stadium:
        stadium.delete()
    else:
        raise HTTPException(status_code=404, detail="stadium not found")
    return {'result': True}


@router.get('/stadiums/{stadium_id}')
def show_stadium(stadium_id: int):
    stadium = Stadium.objects(id=stadium_id).first()
    if not stadium:
        raise HTTPException(status_code=404, detail=f"there is no stadium with id : {stadium_id}")
    return stadium.to_mongo()
