# Author: Louis Pampin
# Last modified: 2025-03-22

import os
import csv
from django.core.management.base import BaseCommand
from apps.play_screen.models import QuizLocation  # Absolute import to avoid Pylint import issues

class Command(BaseCommand):
    help = "Import location data from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), "../../../play_screen/QuizLocations.csv")  # Absolute path
        file_path = os.path.abspath(file_path)

        QuizLocation.objects.all().delete()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                QuizLocation.objects.update_or_create(
                    locationID = row["locationID"],
                    locationName = row["locationName"],
                    latitude = row["latitude"],
                    longitude = row["longitude"],
                    quizID = row["quizID"]
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported quiz location data!"))