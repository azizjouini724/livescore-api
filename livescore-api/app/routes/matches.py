from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.match import Match
from app.services.api_football import APIFootballService

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/live")
def get_live_matches(db: Session = Depends(get_db)):
    """Get live matches"""
    try:
        matches = db.query(Match).filter(Match.status == "live").all()
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/upcoming")
def get_upcoming_matches(db: Session = Depends(get_db), days: int = 7):
    """Get matches in next X days"""
    try:
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=days)
        
        matches = db.query(Match).filter(
            (Match.status == "not_started") &
            (Match.match_date >= start_date) &
            (Match.match_date <= end_date)
        ).order_by(Match.match_date).all()
        
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/finished")
def get_finished_matches(db: Session = Depends(get_db), limit: int = 20):
    """Get finished matches"""
    try:
        matches = db.query(Match).filter(
            Match.status == "finished"
        ).order_by(Match.match_date.desc()).limit(limit).all()
        
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{match_id}")
def get_match_detail(match_id: int, db: Session = Depends(get_db)):
    """Get match detail"""
    try:
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        return match
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{league_id}/{season}")
def sync_matches(league_id: int, season: int, db: Session = Depends(get_db)):
    """Sync matches from API-FOOTBALL"""
    try:
        data = APIFootballService.get_fixtures(league_id, season)
        
        if data['response']:
            for fixture in data['response']:
                # Check if match exists
                existing = db.query(Match).filter(
                    Match.api_id == fixture['fixture']['id']
                ).first()
                
                if not existing:
                    match = Match(
                        api_id=fixture['fixture']['id'],
                        home_team_id=fixture['teams']['home']['id'],
                        away_team_id=fixture['teams']['away']['id'],
                        home_team_name=fixture['teams']['home']['name'],
                        away_team_name=fixture['teams']['away']['name'],
                        home_goals=fixture['goals']['home'],
                        away_goals=fixture['goals']['away'],
                        status=fixture['fixture']['status']['short'].lower(),
                        competition_id=fixture['league']['id'],
                        competition_name=fixture['league']['name'],
                        season=fixture['league']['season'],
                        round=fixture['league'].get('round'),
                        venue=fixture['fixture'].get('venue', {}).get('name'),
                        referee=fixture['fixture'].get('referee'),
                        match_date=datetime.fromisoformat(fixture['fixture']['date'].replace('Z', '+00:00'))
                    )
                    db.add(match)
            
            db.commit()
            return {"status": "success", "synced": len(data['response'])}
        
        return {"status": "success", "synced": 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))