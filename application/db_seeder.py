import argparse
import logging
import os

import django
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "staff.settings")

django.setup()

from django_seed import Seed
import random
from employees.models import Employee, Relation


def parse():
    parser = argparse.ArgumentParser(description='Database seeder')
    parser.add_argument('-n', '--number', type=int, default=20, help='Number of employees to seed')
    argsfromline = parser.parse_args()
    return argsfromline


args = parse()
seeder = Seed.seeder()

seeder.add_entity(Employee, args.number, {
    'name': lambda x: seeder.faker.user_name(),
    'user_name': lambda x: seeder.faker.user_name(),
    'password': 'pbkdf2_sha256$320000$OODaBz9P6MkCK7ClsumQ2x$mMronEWwS384+rc61Etl5/l6QuRCaZwrnwEMqMfI0lo',
    'position': lambda x: random.choice(['dev', 'qa', 'ba']),
    'employment_date': lambda x: seeder.faker.date_time(),
    'monthly_salary': lambda x: random.randint(0, 1000),
    'paid_salary': 0,
    'api_user': lambda x: random.choice([True, False]),
    'is_active': True,
    'is_admin': False,
})
seeder.add_entity(Relation, args.number, {
    'level': lambda x: random.choice([0, 1, 2, 3, 4]),
})

try:
    inserted_pks = seeder.execute()
except ValidationError as e:
    logging.warning(e)
