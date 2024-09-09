from django.db import connection
from django.conf import settings
from elasticsearch import Elasticsearch


es = Elasticsearch([settings.ELASTICSEARCH_DSL['default']['hosts']])


def index_product(product):
    product_data = {
        'name': product.name,
        'price': float(product.price),
    }
    es.index(index='products', id=product.id, body=product_data)


def search_product(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name"]
            }
        }
    }
    result = es.search(index='products', body=body)
    return result['hits']['hits']


def get_product_by_id(product_id: int):
    try:
        result = es.get(index='products', id=product_id)
        return result['_source']
    except Exception:
        return None


def create_order_product(product_id, start_date, end_date, rental_price, rental_duration):
    query = """
        INSERT INTO "order" (start_date, end_date)
        VALUES (%s, %s)
        RETURNING id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        order_id = cursor.fetchone()[0]

    query = """
        INSERT INTO order_product (order_id, product_id, rental_price, rental_duration)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [order_id, product_id, rental_price, rental_duration])
        order_product_id = cursor.fetchone()[0]

    return order_product_id


def get_rental_sum_for_products(start_date, end_date):
    query = """
        SELECT product.name, SUM(order_product.rental_price * order_product.rental_duration) AS total_rental_income
        FROM product
        JOIN order_product ON product.id = order_product.product_id
        JOIN "order" ON order_product.order_id = "order".id
        WHERE "order".start_date >= %s AND "order".end_date <= %s
        GROUP BY product.name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        return cursor.fetchall()


def get_available_periods_for_product(product_id):
    query = """
        SELECT available_period.start_date, available_period.end_date
        FROM (
            SELECT lag("order".end_date, 1) OVER (ORDER BY "order".start_date) AS start_date, 
                   "order".start_date AS end_date
            FROM "order"
            JOIN order_product ON "order".id = order_product.order_id
            WHERE order_product.product_id = %s
        ) available_period
        WHERE available_period.start_date IS NOT NULL
        AND available_period.start_date < available_period.end_date;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [product_id])
        return cursor.fetchall()


def get_total_rental_income(start_date, end_date):
    query = """
        SELECT SUM(order_product.rental_price * order_product.rental_duration) AS total_rental_income
        FROM "order"
        JOIN order_product ON "order".id = order_product.order_id
        WHERE "order".start_date >= %s AND "order".end_date <= %s;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [start_date, end_date])
        return cursor.fetchone()
