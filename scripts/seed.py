from events.models import Event
from datetime import datetime

def seed_events():
    Event.objects.create(
        title="Sample Event 1",
        description="This is a sample event.",
        date=datetime(2025, 4, 1, 10, 0),
        location="Dhaka"
    )
    Event.objects.create(
        title="Sample Event 2",
        description="Another sample event.",
        date=datetime(2025, 4, 5, 15, 0),
        location="Chittagong"
    )
    print("Database seeded!")

if __name__ == "__main__":
    seed_events()