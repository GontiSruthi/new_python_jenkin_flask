# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:51:03 2021

@author: GontiSruthi
"""


import json
from flask import Flask,jsonify,Response,make_response,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:admin@localhost:3306/devops' #to establish connection with DB

db=SQLAlchemy(app)

class Product(db.Model):
    __tablename__="pyproducts"
    productId=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(40))
    description=db.Column(db.String(60))
    productCode=db.Column(db.String(40))
    price=db.Column(db.Float)
    starRating=db.Column(db.Float)
    imageUrl=db.Column(db.String(40))
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self,productName,description,productCode,price,starRating,imageUrl):
        self.productName=productName
        self.description=description
        self.productCode=productCode
        self.price=price
        self.starRating=starRating
        self.imageUrl=imageUrl
    def __repr__(self):
        return"% self.productId"
        
db.create_all()
        
class ProductSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Product
        sqla_session = db.session
    productId = fields.Number(dump_only=True)#productId has to be auto generated so we use (dump_only=True)
    productName=fields.String(required=True)#required represents as mandatory
    description=fields.String(required=True)
    productCode=fields.String(required=True)
    price=fields.Number(required=True)
    starRating=fields.Number(required=True)
    imageUrl = fields.String(required=True)

@app.route('/products',methods=["POST"])
def createProduct():
    data = request.get_json()
    product_schema=ProductSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"product":result}),201)#ORM (object relational mapping)

@app.route('/products',methods=['GET'])
def getAllProducts():
    get_products=Product.query.all()
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({"products":products}),200)

@app.route('/products/<int:productId>',methods=['GET'])
def getProductById(productId):
    get_product=Product.query.get(productId)
    productSchema=ProductSchema()
    product=productSchema.dump(get_product)
    return make_response(jsonify({"product":product}),200)

@app.route('/products/<int:productId>',methods=['DELETE'])
def deleteProductById(productId):
    get_product=Product.query.get(productId)
    db.session.delete(get_product)
    db.session.commit()
    return make_response(jsonify({"result":"product deleted"}),204)

@app.route('/products/<int:productId>',methods=['PUT'])
def updateProduct(productId):
    data = request.get_json()
    get_product=Product.query.get(productId)
    if data.get('price'):
        get_product.price = data['price']
    db.session.add(get_product)
    db.session.commit()
    
    product_schema=ProductSchema(only=['productId','price'])
    
    result = product_schema.dump(get_product)
    return make_response(jsonify({"product":result}),200)


@app.route('/products/find/<productName>',methods=['GET'])
def getProductsById(productName):
    get_products=Product.query.filter_by(productName=productName)#filter_by is like select * from pyproducts where product name='productname'
    productSchema=ProductSchema(many=True)
    products=productSchema.dump(get_products)
    return make_response(jsonify({"product":products}),200)
    
app.run(port=4000)
    
    
    
    
        
  