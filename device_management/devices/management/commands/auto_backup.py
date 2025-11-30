from datetime import datetime

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Automatically backup database and media files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cleanup", action="store_true", help="Clean up old backups"
        )

    def handle(self, *args, **options):
        self.stdout.write(f"Starting automatic backup at {datetime.now()}")

        try:
            self.stdout.write("Creating database backup...")
            call_command("dbbackup", "--clean")
            self.stdout.write(self.style.SUCCESS("Database backup completed"))

            self.stdout.write("Creating media backup...")
            call_command("mediabackup", "--clean")
            self.stdout.write(self.style.SUCCESS("Media backup completed"))

            if options["cleanup"]:
                self.stdout.write("Cleaning up old backups...")
                call_command("dbbackup", "--clean")
                call_command("mediabackup", "--clean")
                self.stdout.write(self.style.SUCCESS("Cleanup completed"))

            self.stdout.write(
                self.style.SUCCESS(
                    f"Automatic backup completed successfully at {datetime.now()}"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Backup failed: {str(e)}"))
