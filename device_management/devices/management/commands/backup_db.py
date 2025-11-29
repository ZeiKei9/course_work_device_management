import os
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a backup of the PostgreSQL database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            type=str,
            default="backups",
            help="Directory to save backup files",
        )

    def handle(self, *args, **options):
        output_dir = options["output_dir"]

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.stdout.write(
                self.style.SUCCESS(f"Created backup directory: {output_dir}")
            )

        db_config = settings.DATABASES["default"]
        db_name = db_config["NAME"]
        db_user = db_config["USER"]
        db_password = db_config["PASSWORD"]
        db_host = db_config["HOST"]
        db_port = db_config["PORT"]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_{db_name}_{timestamp}.sql"
        backup_path = os.path.join(output_dir, backup_filename)

        env = os.environ.copy()
        env["PGPASSWORD"] = db_password

        try:
            self.stdout.write(f"Creating backup of database: {db_name}")

            command = [
                "pg_dump",
                "-h",
                db_host,
                "-p",
                str(db_port),
                "-U",
                db_user,
                "-F",
                "c",
                "-b",
                "-v",
                "-f",
                backup_path,
                db_name,
            ]

            result = subprocess.run(command, env=env, capture_output=True, text=True)

            if result.returncode == 0:
                file_size = os.path.getsize(backup_path)
                size_mb = file_size / (1024 * 1024)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Backup created successfully: {backup_path} ({size_mb:.2f} MB)"
                    )
                )
            else:
                self.stdout.write(self.style.ERROR(f"Backup failed: {result.stderr}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating backup: {str(e)}"))
