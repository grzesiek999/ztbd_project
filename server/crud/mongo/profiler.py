from pymongo.synchronous.database import Database


def get_last_query_time(db: Database) -> int:
    profile_entry = db.system.profile.find_one(
        {"command.comment": "backend_query"},
        sort=[("ts", -1)]  # Sortowanie po czasie (od najnowszego)
    )

    if profile_entry:
        return profile_entry.get("millis", -1)
    else:
        return -1
