from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    # Valid SpaceStation
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        last_maintenance="2026-04-11T12:00:00",
        power_level=85.5,
        oxygen_level=92.3,
        notes="Operational")

    print(
        "\nSpace Station Data Validation\n"
        "========================================\n"
        "Valid station created:\n"
        f"ID: {station.station_id}\n"
        f"Name: {station.name}\n"
        f"Crew: {station.crew_size} people\n"
        f"Power: {station.power_level}%\n"
        f"Oxygen: {station.oxygen_level}%\n"
        f"Status: {'Operational' if station.is_operational
                   else 'Not Operational'}\n\n"
        "========================================")

    # Invalid SpaceStation
    try:
        SpaceStation(
            station_id="ISS001",
            name="Broken Station",
            crew_size=25,  # ERROR
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance="2024-01-01T12:00:00")

    except ValidationError as e:
        print(
            "Expected validation error:\n"
            f"{e.errors()[0]['msg']}\n")


if __name__ == "__main__":
    main()
