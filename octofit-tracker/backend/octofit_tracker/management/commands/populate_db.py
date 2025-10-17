from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(host='localhost', port=27017)
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create teams
        marvel_team = {'name': 'Team Marvel', 'members': []}
        dc_team = {'name': 'Team DC', 'members': []}
        marvel_team_id = db.teams.insert_one(marvel_team).inserted_id
        dc_team_id = db.teams.insert_one(dc_team).inserted_id

        # Create users (superheroes)
        users = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team_id': marvel_team_id},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team_id': dc_team_id},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team_id': dc_team_id},
        ]
        user_ids = db.users.insert_many(users).inserted_ids

        # Update teams with members
        db.teams.update_one({'_id': marvel_team_id}, {'$set': {'members': user_ids[:2]}})
        db.teams.update_one({'_id': dc_team_id}, {'$set': {'members': user_ids[2:]}})

        # Create activities
        activities = [
            {'user_id': user_ids[0], 'type': 'run', 'distance': 5, 'duration': 30},
            {'user_id': user_ids[1], 'type': 'cycle', 'distance': 20, 'duration': 60},
            {'user_id': user_ids[2], 'type': 'swim', 'distance': 2, 'duration': 45},
            {'user_id': user_ids[3], 'type': 'walk', 'distance': 3, 'duration': 40},
        ]
        db.activities.insert_many(activities)

        # Create leaderboard
        leaderboard = [
            {'team_id': marvel_team_id, 'points': 100},
            {'team_id': dc_team_id, 'points': 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Create workouts
        workouts = [
            {'name': 'Morning Cardio', 'suggested_for': [user_ids[0], user_ids[2]]},
            {'name': 'Strength Training', 'suggested_for': [user_ids[1], user_ids[3]]},
        ]
        db.workouts.insert_many(workouts)

        # Ensure unique index on email
        db.users.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
