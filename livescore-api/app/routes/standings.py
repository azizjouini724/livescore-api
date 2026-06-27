from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.standing import Standing
from app.services.api_football import APIFootballService
from app.schemas.standing import StandingResponse

router = APIRouter(prefix="/standings", tags=["standings"])

@router.get("/{league_id}/{season}", response_model=list[StandingResponse])
def get_standings(league_id: int, season: int, db: Session = Depends(get_db)):
    """Get standings for a league and season"""
    try:
        standings = db.query(Standing).filter(
            (Standing.competition_id == league_id) & 
            (Standing.season == season)
        ).order_by(Standing.rank).all()
        
        if not standings:
            raise HTTPException(status_code=404, detail="Standings not found")
        
        return standings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/competition/{competition_id}", response_model=list[StandingResponse])
def get_standings_by_competition(competition_id: int, db: Session = Depends(get_db)):
    """Get latest standings for a competition"""
    try:
        standings = db.query(Standing).filter(
            Standing.competition_id == competition_id
        ).order_by(Standing.rank).all()
        
        if not standings:
            raise HTTPException(status_code=404, detail="Standings not found")
        
        return standings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{league_id}/{season}")
def sync_standings(league_id: int, season: int, db: Session = Depends(get_db)):
    """Sync standings from API-FOOTBALL"""
    try:
        data = APIFootballService.get_standings(league_id, season)
        
        if data.get('response') and len(data['response']) > 0:
            # Delete old standings
            db.query(Standing).filter(
                (Standing.competition_id == league_id) &
                (Standing.season == season)
            ).delete()
            
            count = 0
            # API v3 returns: response[0].standings = [[group1], [group2]]
            standings_groups = data['response'][0].get('standings', [])
            
            for group in standings_groups:
                for standing in group:
                    team_info = standing.get('team', {})
                    goals_info = standing.get('goals', {})
                    all_stats = standing.get('all', {})
                    
                    standing_obj = Standing(
                        competition_id=league_id,
                        season=season,
                        team_id=team_info.get('id'),
                        team_name=team_info.get('name'),
                        rank=standing.get('rank'),
                        points=standing.get('points'),
                        matches_played=all_stats.get('played', standing.get('played', 0)),
                        wins=all_stats.get('win', standing.get('win', 0)),
                        draws=all_stats.get('draw', standing.get('draw', 0)),
                        losses=all_stats.get('lose', standing.get('lose', 0)),
                        goals_for=goals_info.get('for', 0),
                        goals_against=goals_info.get('against', 0),
                        goal_difference=goals_info.get('diff', standing.get('goalsDiff', 0))
                    )
                    db.add(standing_obj)
                    count += 1
            
            db.commit()
            return {"status": "success", "synced": count}
        
        return {"status": "success", "synced": 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))