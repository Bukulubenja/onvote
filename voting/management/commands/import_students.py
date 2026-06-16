import csv
import random
import string
import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from voting.models import Voter,Class


class Command(BaseCommand):
    help = "Import students and create voter accounts"

    def handle(self, *args, **kwargs):

        file_path = os.path.join(os.getcwd(), 'students.csv')

        self.stdout.write(f"Opening file: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                self.stdout.write(f"CSV HEADERS: {reader.fieldnames}")

                count = 0

                # ✅ OPEN OUTPUT FILE ONCE AND KEEP IT OPEN DURING LOOP
                with open("student_passwords.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["student_id", "password"])

                    for row in reader:

                        # FIX BOM ISSUE
                        row = {k.replace('\ufeff', ''): v for k, v in row.items()}

                        student_id = (row.get('student_id') or "").strip()
                        first_name = (row.get('first_name') or "").strip()
                        last_name = (row.get('last_name') or "").strip()
                        class_name = (row.get('class_name') or "S5").strip()
                        class_obj, created = Class.objects.get_or_create(name=class_name
)

                        if not student_id:
                            continue

                        # skip duplicates
                        if User.objects.filter(username=student_id).exists():
                            self.stdout.write(
                                self.style.WARNING(f"{student_id} already exists - skipped")
                            )
                            continue

                        # generate password
                        password = ''.join(
                            random.choices(string.ascii_letters + string.digits, k=8)
                        )

                        # create user
                        user = User.objects.create_user(
                            username=student_id,
                            password=password,
                            first_name=first_name,
                            last_name=last_name
                        )

                        # create voter
                        Voter.objects.create(
                            user=user,
                            student_id=student_id,
                            class_name=class_obj
                        )

                        # save to file
                        writer.writerow([student_id, password])

                        count += 1
                        self.stdout.write(f"{student_id} -> {password}")

                self.stdout.write(self.style.SUCCESS(f"Imported {count} students"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("students.csv NOT FOUND in project root"))