from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, matches, teams, players, competitions, standings, favorites, profile

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LiveScore API",
    description="Football LiveScore API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(teams.router)
app.include_router(players.router)
app.include_router(competitions.router)
app.include_router(standings.router)
app.include_router(favorites.router)
app.include_router(profile.router)

@app.get("/")
def root():
    return {"message": "LiveScore API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)