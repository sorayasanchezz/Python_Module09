from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum
from datetime import datetime


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_args(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        if not any(member.rank in [Rank.commander,
                                   Rank.captain] for member in self.crew):
            raise ValueError("Mission must have at "
                             "least one Commander or Captain")

        if self.duration_days > 365:
            experienced = [m for m in self.crew if m.years_experience >= 5]
            if len(experienced) < len(self.crew) / 2:
                raise ValueError("Need at least 50% experienced crew")

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    crew = [
        CrewMember(
            member_id="C01",
            name="Sarah Connor",
            rank="commander",
            age=40,
            specialization="Mission Command",
            years_experience=10,
            is_active=True),

        CrewMember(
            member_id="C02",
            name="John Smith",
            rank="lieutenant",
            age=35,
            specialization="Navigation",
            years_experience=6,
            is_active=True),

        CrewMember(
            member_id="C03",
            name="Alice Johnson",
            rank="officer",
            age=30,
            specialization="Engineering",
            years_experience=5,
            is_active=True)]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2024-06-01T10:00:00",
        duration_days=900,
        crew=crew,
        budget_millions=2500.0)

    print(
        "\nSpace Mission Crew Validation\n"
        "=========================================\n"
        "Valid mission created:\n"
        f"Mission: {mission.mission_name}\n"
        f"ID: {mission.mission_id}\n"
        f"Destination: {mission.destination}\n"
        f"Duration: {mission.duration_days} days\n"
        f"Budget: ${mission.budget_millions}M\n"
        f"Crew size: {len(mission.crew)}\n"
        "Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) "
              f"- {member.specialization}")
    print("\n=========================================")


def error_case() -> None:
    try:
        bad_crew = [
            CrewMember(
                member_id="C10",
                name="Bob",
                rank="officer",
                age=25,
                specialization="Engineering",
                years_experience=2,
                is_active=True)]

        SpaceMission(
            mission_id="M_BAD",
            mission_name="Failed Mission",
            destination="Moon",
            launch_date="2024-06-01T10:00:00",
            duration_days=100,
            crew=bad_crew,
            budget_millions=100.0)

    except ValidationError as e:
        print(
            "Expected validation error:\n"
            f"{e.errors()[0]['msg']}\n")


if __name__ == "__main__":
    main()
    error_case()
