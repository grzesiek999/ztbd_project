from sqlalchemy import text

def reset_sequence(db, param: str):
    db.execute(text(param))
    db.commit()