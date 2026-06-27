from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.player import Player
from app.services.api_football import APIFootballService
from app.schemas.player import PlayerResponse

router = APIRouter(prefix="/players", tags=["players"])

@router.get("/", response_model=list[PlayerResponse])
def get_all_players(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    """Get all players from database"""
    try:
        players = db.query(Player).offset(skip).limit(limit).all()
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player_detail(player_id: int, db: Session = Depends(get_db)):
    """Get player detail by ID"""
    try:
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api-id/{api_id}", response_model=PlayerResponse)
def get_player_by_api_id(api_id: int, db: Session = Depends(get_db)):
    """Get player by API-FOOTBALL ID"""
    try:
        player = db.query(Player).filter(Player.api_id == api_id).first()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{team_id}/{season}")
def sync_players(team_id: int, season: int, db: Session = Depends(get_db)):
    """Sync players from API-FOOTBALL by team"""
    try:
        data = APIFootballService.get_players(team_id, season)
        
        if data.get('response'):
            count = 0
            for player_data in data['response']:
                player_info = player_data['player']
                
                # Check if player exists
                existing = db.query(Player).filter(Player.api_id == player_info['id']).first()
                
                if not existing:
                    player = Player(
                        api_id=player_info['id'],
                        name=player_info['name'],
                        firstname=player_info.get('firstname'),
                        lastname=player_info.get('lastname'),
                        age=player_info.get('age'),
                        birth_date=player_info.get('birth', {}).get('date') if player_info.get('birth') else None,
                        nationality=player_info.get('nationality'),
                        height=player_info.get('height'),
                        weight=player_info.get('weight'),
                        injured=1 if player_info.get('injured') else 0,
                        photo=player_info.get('photo')
                    )
                    db.add(player)
                    count += 1
            
            db.commit()
            return {"status": "success", "synced": count}
        
        return {"status": "success", "synced": 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))