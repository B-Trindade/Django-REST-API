"""
Test custom Django Management Commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Tests commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database to be ready."""
        patched_check.return_value = True

        call_command('wait_for_db')  # runs the wait_for_db command

        patched_check.assert_called_once_with(databases=['default'])
        pass

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""

        #Psycopg2Error usually happens when PostgreSQL 
        # is not ready to accept connections
        #OperationalError happens when the database is ready but
        # the testing database has not been created yet (raised by Django)

        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # The first 2 times are expected to raise Psycopg2Error and 
        #  the following 3 times should raise OpErr (in 6th we get OK)
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

        pass
