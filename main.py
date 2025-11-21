from fastapi import FastAPI
from api.v1.auth import router as auth_router
from api.v1.journals import router as journals_router
from api.v1.karma import router as karma_router
from api.v1.nibbana import router as nibbana_router
from api.v1.ai import router as ai_router

app = FastAPI(title="Putthochain Full API")

app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(journals_router, prefix='/journals', tags=['Journals'])
app.include_router(karma_router, prefix='/karma', tags=['Karma'])
app.include_router(nibbana_router, prefix='/nibbana', tags=['Nibbana'])
app.include_router(ai_router, prefix='/ai', tags=['AI'])

@app.get('/')
def root():
    return {"message": "Putthochain Full Backend Running"}