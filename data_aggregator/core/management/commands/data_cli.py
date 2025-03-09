from django.core.management.base import BaseCommand
from django.db import connections
import MySQLdb
import json

class Command(BaseCommand):
    help = 'CLI interface for data aggregation system'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform: test_connection, query')
        parser.add_argument('--database', type=str, help='Database to query (central or remote)', required=False)
        parser.add_argument('--query', type=str, help='SQL query to execute', required=False)

    def handle(self, *args, **options):
        action = options['action']

        if action == 'test_connection':
            self._test_connections()
        elif action == 'query':
            if not options.get('database') or not options.get('query'):
                self.stdout.write(self.style.ERROR('Both --database and --query are required for query action'))
                return
            self._execute_query(options['database'], options['query'])
        else:
            self.stdout.write(self.style.ERROR(f'Unknown action: {action}'))

    def _test_connections(self):
        # Test central database
        self.stdout.write("\nTesting connection to central database...")
        try:
            db = MySQLdb.connect(
                host='localhost',
                user='root',
                passwd='tiger',
                port=3306
            )
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f"SUCCESS: Connected to central database (MySQL {version[0]})"))
            cursor.close()
            db.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: Could not connect to central database: {str(e)}"))

        # Test remote database
        self.stdout.write("\nTesting connection to remote database...")
        try:
            db = MySQLdb.connect(
                host='192.168.161.174',
                user='root',
                passwd='uyobaby123',
                port=3306
            )
            cursor = db.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f"SUCCESS: Connected to remote database (MySQL {version[0]})"))
            cursor.close()
            db.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"FAILED: Could not connect to remote database: {str(e)}"))

    def _execute_query(self, database, query):
        try:
            config = {
                'central': {
                    'host': 'localhost',
                    'user': 'root',
                    'passwd': 'tiger',
                    'port': 3306,
                    'db': 'central_db'
                },
                'remote': {
                    'host': '192.168.161.174',
                    'user': 'root',
                    'passwd': 'uyobaby123',
                    'port': 3306,
                    'db': 'source2_db'
                }
            }

            if database not in config:
                raise ValueError(f"Invalid database. Use 'central' or 'remote'")

            db = MySQLdb.connect(**config[database])
            cursor = db.cursor()
            cursor.execute(query)
            
            if cursor.description:  # If the query returns results
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                
                # Print results in a tabular format
                self.stdout.write('\n' + '\t'.join(columns))
                self.stdout.write('-' * (len(columns) * 12))
                for row in rows:
                    self.stdout.write('\t'.join(str(val) for val in row))
            else:
                self.stdout.write(self.style.SUCCESS("Query executed successfully (no results to display)"))
            
            cursor.close()
            db.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error executing query: {str(e)}'))
