from fastapi import APIRouter, HTTPException, Response, Depends
from sqlalchemy import true
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlmodel import select
from db import session
from models.gem_models import Gem, GemProperties, GemPatch, GemType
import repos.gem_repository as gem_repository
from auth.auth import AuthHandler
from typing import Optional

router = APIRouter(prefix='/gems', tags=['Gems'])
auth_handler = AuthHandler()

@router.get('/')
def get_gems(lte: Optional[int]=None, gte: Optional[int]=None, type: Optional[GemType] = None):
    gems_statement = select(Gem, GemProperties).join(GemProperties)
    if lte:
        gems_statement = gems_statement.where(Gem.price <= lte)
    if gte:
        gems_statement = gems_statement.where(Gem.price >= gte)
    if type:
        gems_statement = gems_statement.where(Gem.type == type)
    gems = session.exec(gems_statement).all()
    return {'gems': gems}

@router.get('/{gem_id}')
def get_gem_by_id(gem_id: int):
    gem = session.get(Gem, gem_id)
    if not gem:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'Gem with an id: {gem_id} was not found')
    return {'gem': gem}

@router.post('/')
def create_gem(gem_pr: GemProperties, gem: Gem, current_user=Depends(auth_handler.get_current_user)):
    gem_properties = GemProperties(size=gem_pr.size, color=gem_pr.color, clarity=gem_pr.clarity)
    session.add(gem_properties)
    session.commit()
    session.refresh(gem_properties)
    gem_ = Gem(price=gem.price, type=gem.type, is_available=gem.is_available, properties_id=gem_properties.id, seller_id=current_user.id)
    session.add(gem_)
    session.commit()
    session.refresh(gem_)
    if not current_user.is_seller: 
        current_user.is_seller = true
    return gem_

@router.patch('/{gem_id}')
def patch_gem(gem_id: int, gem: GemPatch):
    gem_found = session.get(Gem, gem_id)
    if not gem_found:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Gem with an id: {gem_id} was not found')
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=f'Gem with an id: {gem_id} was not found')
    update_data = gem.dict(exclude_unset=True)
    for key, val in update_data.items():
        gem_found.__setattr__(key, val)
    session.commit()
    session.refresh(gem_found)
    return gem_found

@router.put('/{gem_id}')
def update_gem(gem_id: int, gem: Gem):
    gem_found = session.get(Gem, gem_id)
    if not gem_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Gem with an id: {gem_id} was not found')
    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop('id', None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    session.refresh(gem_found)
    return gem_found

@router.delete('/{gem_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_gem(gem_id: int, current_user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, gem_id)
    if not gem_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Gem with an id: {gem_id} was not found')
    if gem_found.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete this gem")
    session.delete(gem_found)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/seller/me')
def get_my_gems(current_user=Depends(auth_handler.get_current_user)):
    if not current_user.is_seller:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content='You are not a seller')
    statement = select(Gem, GemProperties).where(Gem.properties_id == GemProperties.id)
    statement = statement.where(Gem.seller_id == current_user.id)
    result = session.exec(statement)
    return result.all()


