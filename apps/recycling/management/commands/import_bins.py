# Author: Louis Pampin
# Last modified: 2025-03-22

import os
import csv
from django.core.management.base import BaseCommand
from apps.recycling.models import Bin  # Absolute import to avoid Pylint import issues

class Command(BaseCommand):
    help = "Import location data from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), "../../../recycling/BinLocations.csv")  # Absolute path
        file_path = os.path.abspath(file_path)

        Bin.objects.all().delete()

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Bin.objects.update_or_create(
                    binID = row["binID"],
                    latitude = row["latitude"],
                    longitude = row["longitude"],
                    binIdentifier = row["binIdentifier"]
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported bin location data!"))