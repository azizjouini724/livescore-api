from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.services.api_football import APIFootballService
from app.schemas.team import TeamResponse

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamResponse])
def get_all_teams(db: Session = Depends(get_db), skip: int = 0, limit: int = 50):
    """Get all teams from database"""
    try:
        teams = db.query(Team).offset(skip).limit(limit).all()
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{team_id}", response_model=TeamResponse)
def get_team_detail(team_id: int, db: Session = Depends(get_db)):
    """Get team detail by ID"""
    try:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api-id/{api_id}", response_model=TeamResponse)
def get_team_by_api_id(api_id: int, db: Session = Depends(get_db)):
    """Get team by API-FOOTBALL ID"""
    try:
        team = db.query(Team).filter(Team.api_id == api_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync/{league_id}/{season}")
def sync_teams(league_id: int, season: int, db: Session = Depends(get_db)):
    """Sync teams from API-FOOTBALL"""
    try:
        data = APIFootballService.get_teams(league_id, season)
        
        if data.get('response'):
            count = 0
            for team_data in data['response']:
                team_info = team_data['team']
                
                # Check if team exists
                existing = db.query(Team).filter(Team.api_id == team_info['id']).first()
                
                if not existing:
                    team = Team(
                        api_id=team_info['id'],
                        name=team_info['name'],
                        code=team_info.get('code'),
                        country=team_info.get('country'),
                        founded=team_info.get('founded'),
                        national=1 if team_info.get('national') else 0,
                        logo=team_info.get('logo'),
                        venue_name=team_data.get('venue', {}).get('name'),
                        venue_city=team_data.get('venue', {}).get('city'),
                        venue_capacity=team_data.get('venue', {}).get('capacity')
                    )
                    db.add(team)
                    count += 1
            
            db.commit()
            return {"status": "success", "synced": count}
        
        return {"status": "success", "synced": 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))