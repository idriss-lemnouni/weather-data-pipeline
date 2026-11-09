from csv import DictReader
from datetime import date
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent


def nullable(value):
    return None if value in ("", "NA") else float(value)


def ingest(source, destination):
    missing = {"ozone_ppb": 0, "solar_langley": 0}
    readings = []
    dates = set()
    with source.open(encoding="utf-8-sig", newline="") as stream:
        for row in DictReader(stream):
            day = date(1973, int(row["Month"]), int(row["Day"])).isoformat()
            if day in dates:
                raise ValueError(f"Date dupliquée : {day}")
            dates.add(day)
            ozone = nullable(row["Ozone"])
            solar = nullable(row["Solar.R"])
            missing["ozone_ppb"] += ozone is None
            missing["solar_langley"] += solar is None
            temp = (float(row["Temp"]) - 32) * 5 / 9
            wind = float(row["Wind"]) * 0.44704
            readings.append((day, ozone, solar, wind, temp))

    with sqlite3.connect(destination) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS observations (
            day TEXT PRIMARY KEY, ozone_ppb REAL, solar_langley REAL,
            wind_m_s REAL NOT NULL, temperature_c REAL NOT NULL
        )""")
        connection.execute("DELETE FROM observations")
        connection.executemany("INSERT INTO observations VALUES (?, ?, ?, ?, ?)", readings)
    return {"rows": len(readings), "missing": missing, "first_day": min(dates), "last_day": max(dates)}


if __name__ == "__main__":
    report = ingest(ROOT / "airquality.csv", ROOT / "observations.sqlite")
    (ROOT / "quality.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
