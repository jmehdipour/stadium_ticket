from fastapi import APIRouter, HTTPException, Depends
from mongoengine.queryset.visitor import Q

from src.api.middlewares import is_admin
from src.api.schemas import MatchIn
from src.data.connections.mongodb import counter
from src.data.models.mongodb import Match, Stadium

router = APIRouter()


@router.get('/matches')
def get_all_matches(size: int = 10, last_id: int = None, first_id: int = None):
    if first_id and not last_id:
        matches = Match.objects(id__gt=first_id)
    elif not first_id and last_id:
        matches = Match.objects(id__lt=last_id)
    else:
        matches = Match.objects()

    match_dict_list = [match.to_mongo() for match in matches.order_by('-id').limit(size)]
    return match_dict_list


@router.post('/matches', dependencies=[Depends(is_admin)])
def create_match(match_data: MatchIn):
    stadium = Stadium.objects(id=match_data.stadium_id).first()
    if not stadium:
        raise HTTPException(
            status_code=422,
            detail=f"there is no stadium with id: {match_data.stadium_id}"
        )
    matches = Match.objects(
        Q(starts_at__lt=match_data.starts_at) & Q(ends_at__gt=match_data.starts_at) |
        Q(starts_at__lt=match_data.ends_at) & Q(ends_at__gt=match_data.ends_at)
    )
    if list(matches):
        raise HTTPException(
            status_code=422,
            detail=f"there is overlap on match time with another match on this stadium"
        )

    try:
        mongo_match = Match(id=counter('match'), **match_data.dict())
        mongo_match.save()
    except Exception as ex:
        raise HTTPException(status_code=500, detail="internal server error")
    return mongo_match.to_mongo


@router.get('/matches/{match_id}')
async def get_match(match_id: int):
    match = Match.objects(id=match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="match not found")
    return match.to_mongo()


@router.delete('/matches/{match_id}', dependencies=[Depends(is_admin)])
async def delete_match(match_id: int):
    match = Match.objects(id=match_id).first()
    if match:
        match.delete()
    else:
        raise HTTPException(status_code=404, detail="match not found")
    return {"result": True}
