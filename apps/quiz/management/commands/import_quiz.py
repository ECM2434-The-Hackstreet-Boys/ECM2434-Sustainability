# Author: Louis Pampin
# Last modified: 2025-02-22

import os
import csv
from django.core.management.base import BaseCommand
from apps.quiz.models import quiz  # Absolute import to avoid Pylint import issues

class Command(BaseCommand):
    help = "Import quiz data from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), "../../../quiz/sustainabilityQuestions.csv")  # Absolute path
        file_path = os.path.abspath(file_path)

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                quiz.objects.get_or_create(
                    question=row["question"],
                    answer=row["answer"],
                    other1=row["other1"],
                    other2=row["other2"],
                    other3=row["other3"],
                    landmark_id=row["landmark_id"]
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported quiz data!"))
