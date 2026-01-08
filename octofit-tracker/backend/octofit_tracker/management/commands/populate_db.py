from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from django.apps import apps

from djongo import models

from octofit_tracker import settings

# Sample data for users, teams, activities, leaderboard, and workouts
USERS = [
    {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
    {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
    {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
    {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
    {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
    {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
]

TEAMS = [
    {"name": "Marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
    {"name": "DC", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
]

ACTIVITIES = [
    {"user_email": "superman@dc.com", "activity": "Flight", "duration": 60},
    {"user_email": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
    {"user_email": "ironman@marvel.com", "activity": "Suit Training", "duration": 50},
]

LEADERBOARD = [
    {"team": "Marvel", "points": 300},
    {"team": "DC", "points": 250},
]

WORKOUTS = [
    {"name": "Strength Training", "suggested_for": "DC"},
    {"name": "Agility Drills", "suggested_for": "Marvel"},
]

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert test data
        db.users.insert_many(USERS)
        db.teams.insert_many(TEAMS)
        db.activities.insert_many(ACTIVITIES)
        db.leaderboard.insert_many(LEADERBOARD)
        db.workouts.insert_many(WORKOUTS)

        # Ensure unique index on email for users
        db.users.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
