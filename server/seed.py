#!usr/bin/env python3

from app import app
from models import db

with app.app_context():
    print("Starting seed...")

    # reset data and add new example data here

    print("Seed complete.")