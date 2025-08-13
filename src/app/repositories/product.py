from flask import jsonify, request
from sqlalchemy import UUID
from app.database import db
from app.mappers.product import ProductMapper
from app.models.product import Product

class ProductRepository:
    @staticmethod
    def create(product):
        try:
            db.session.add(product)
            db.session.commit()
            return product
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all():
        return Product.query.all()

    @staticmethod
    def get_by_id(product_id):
        return Product.query.filter_by(id=product_id).first()

    @staticmethod
    def delete(product):
        db.session.delete(product)
        db.session.commit()


    @staticmethod
    def reduce_stock(product_id, quantity):
        product = Product.query.get(product_id)
        if not product:
            raise ValueError("Product not found")

        if product.available_stock < quantity:
            raise ValueError("Not enough stock available")

        product.available_stock -= quantity
        db.session.commit()
        return product

