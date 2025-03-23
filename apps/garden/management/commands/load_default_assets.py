from django.core.management.base import BaseCommand
from apps.garden.models import Block

class Command(BaseCommand):
    help = "Load default game assets into the database"

    def handle(self, *args, **kwargs):
        default_assets = [

            {"name": "Grass", "visibleName":"Grass", "blockPath": "blocks/tileGrass.png", "cost": 0, "value": 0},
            {"name": "Tree", "visibleName":"Tree", "blockPath": "blocks/tileTree.png", "cost": 10, "value": 5},
            {"name": "Flower", "visibleName":"Flowers", "blockPath": "blocks/tileFlower.png", "cost": 20, "value": 10},
            {"name": "Pink Flower", "visibleName":"Pink Flower", "blockPath": "blocks/tileFlowerPink.png", "cost": 30, "value": 15},

        ]

        for asset in default_assets:
            obj, created = Block.objects.get_or_create(name=asset["name"], defaults={"visibleName":asset['visibleName'], "blockPath": asset["blockPath"], "cost": asset["cost"], "value": asset["value"]})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added: {asset["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Skipped (already exists): {asset["name"]}'))

        self.stdout.write(self.style.SUCCESS("Default assets loading complete!"))
