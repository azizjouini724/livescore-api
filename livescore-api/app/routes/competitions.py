from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.competition import Competition
from app.services.api_football import APIFootballService
from app.schemas.competition import CompetitionResponse

router = APIRouter(prefix="/competitions", tags=["competitions"])

@router.get("/", response_model=list[CompetitionResponse])
def get_all_competitions(db: Session = Depends(get_db)):
    """Get all competitions"""
    try:
        competitions = db.query(Competition).all()
        return competitions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition_detail(competition_id: int, db: Session = Depends(get_db)):
    """Get competition detail"""
    try:
        competition = db.query(Competition).filter(Competition.id == competition_id).first()
        if not competition:
            raise HTTPException(status_code=404, detail="Competition not found")
        return competition
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/sync")
def sync_competitions(db: Session = Depends(get_db)):
    """Sync competitions from API-FOOTBALL"""
    try:
        data = APIFootballService.get_leagues()
        
        if data.get('response'):
            count = 0
            for comp_data in data['response']:
                league = comp_data['league']
                
                existing = db.query(Competition).filter(
                    Competition.api_id == league['id']
                ).first()
                
                if not existing:
                    competition = Competition(
                        api_id=league['id'],
                        name=league['name'],
                        country=league.get('country'),
                        logo=league.get('logo'),
                        type=league.get('type'),
                        season=comp_data['seasons'][0]['year'] if comp_data.get('seasons') else 2024,
                        current_season_start=comp_data.get('seasons', [{}])[0].get('start'),
                        current_season_end=comp_data.get('seasons', [{}])[0].get('end')
                    )
                    db.add(competition)
                    count += 1
            
            db.commit()
            return {"status": "success", "synced": count}
        
        return {"status": "success", "synced": 0}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))