from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import MySQLdb
from django.conf import settings

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def execute_query(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            database = data.get('database', 'central')
            query_type = data.get('query_type', 'custom')
            
            if query_type == 'custom':
                field = data.get('field', '')
                operator = data.get('operator', '')
                value = data.get('value', '')
                table = data.get('table', '')
                
                # Build the query based on user input
                query = f"SELECT * FROM {table}"
                if field and operator and value:
                    query += f" WHERE {field} {operator} "
                    # Add quotes if value is string
                    if not value.replace('.', '').isdigit():
                        query += f"'{value}'"
                    else:
                        query += value
            else:
                # Predefined business queries
                query = get_business_query(query_type, database)
                if not query:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid query type'
                    }, status=400)

            # Get database configuration
            db_config = settings.DATABASES[database]
            
            # Connect to database
            db = MySQLdb.connect(
                host=db_config['HOST'],
                user=db_config['USER'],
                passwd=db_config['PASSWORD'],
                db=db_config['NAME'],
                port=int(db_config.get('PORT', 3306))
            )
            
            cursor = db.cursor()
            cursor.execute(query)
            
            # Get column names
            columns = [col[0] for col in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                results.append(dict(zip(columns, row)))
            
            cursor.close()
            db.close()
            
            return JsonResponse({
                'status': 'success',
                'data': results,
                'columns': columns
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def get_business_query(query_type, database):
    queries = {
        'monthly_sales': """
            SELECT 
                DATE_FORMAT(s.sale_date, '%Y-%m') as month,
                p.category,
                COUNT(*) as total_sales,
                SUM(s.quantity) as units_sold,
                SUM(s.total_amount) as revenue,
                c.country
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY DATE_FORMAT(s.sale_date, '%Y-%m'), p.category, c.country
            ORDER BY month
        """,
        'inventory_status': """
            SELECT 
                p.category,
                COUNT(*) as product_count,
                SUM(p.stock_quantity) as total_stock,
                SUM(p.stock_quantity * p.unit_price) as inventory_value
            FROM products p
            GROUP BY p.category
        """,
        'department_performance': """
            SELECT 
                d.dept_name,
                COUNT(e.emp_id) as employee_count,
                d.budget,
                d.location,
                AVG(e.salary) as avg_salary
            FROM departments d
            LEFT JOIN employees e ON d.dept_name = e.department
            GROUP BY d.dept_name, d.budget, d.location
        """,
        'customer_distribution': """
            SELECT 
                c.country,
                COUNT(DISTINCT c.customer_id) as customer_count,
                COUNT(s.sale_id) as total_orders,
                SUM(s.total_amount) as total_revenue
            FROM customers c
            LEFT JOIN sales s ON c.customer_id = s.customer_id
            GROUP BY c.country
        """
    }
    return queries.get(query_type)

@csrf_exempt
def get_tables(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            database = data.get('database', 'central')
            
            # Get database configuration
            db_config = settings.DATABASES[database]
            
            # Connect to database
            db = MySQLdb.connect(
                host=db_config['HOST'],
                user=db_config['USER'],
                passwd=db_config['PASSWORD'],
                db=db_config['NAME'],
                port=int(db_config.get('PORT', 3306))
            )
            
            cursor = db.cursor()
            cursor.execute("SHOW TABLES")
            
            # Fetch all tables
            tables = [table[0] for table in cursor.fetchall()]
            
            cursor.close()
            db.close()
            
            return JsonResponse({
                'status': 'success',
                'tables': tables
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def get_columns(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            database = data.get('database', 'central')
            table = data.get('table', '')
            
            if not table:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Table name is required'
                }, status=400)
            
            # Get database configuration
            db_config = settings.DATABASES[database]
            
            # Connect to database
            db = MySQLdb.connect(
                host=db_config['HOST'],
                user=db_config['USER'],
                passwd=db_config['PASSWORD'],
                db=db_config['NAME'],
                port=int(db_config.get('PORT', 3306))
            )
            
            cursor = db.cursor()
            cursor.execute(f"DESCRIBE {table}")
            
            # Fetch all columns
            columns = [column[0] for column in cursor.fetchall()]
            
            cursor.close()
            db.close()
            
            return JsonResponse({
                'status': 'success',
                'columns': columns
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
