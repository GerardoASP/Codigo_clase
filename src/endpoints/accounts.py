from flask import Blueprint, request
from http import HTTPStatus
import werkzeug
import sqlalchemy
from src.database import db
from src.models.account import Account, account_schema,accounts_schema

accounts = Blueprint("accounts",__name__,url_prefix="/api/v1/accounts")

@accounts.get("/")
def read_all():
    accounts = Account.query.order_by(Account.code).all()
    
    return {"data":accounts_schema.dump(accounts)}, HTTPStatus.OK

@accounts.get("/<string:code>")
def read_one(code):
    account = Account.query.filter_by(code=code).first()
    
    if(not account):
        return {
            "error":"Resource not found"
        }, HTTPStatus.NOT_FOUND
    
    return {"data":account_schema.dump(account)},HTTPStatus.OK

@accounts.post("/")
def create():
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {
            "error":"Post body JSON Data not found",
            "message":str(e)
        },HTTPStatus.BAD_REQUEST

    account = Account(code=request.get_json().get("code",None),
                observations = request.get_json().get("observations",None),
                balance = request.get_json().get("balance",None),
                registered_phone = request.get_json().get("registered_phone",None))
    try:
        db.session.add(account)
    except sqlalchemy.ext.IntegrityError as e:
        return {
            "error":"Invalid resource values",
            "message":str(e)
        },HTTPStatus.BAD_REQUEST
    return {"data":account_schema.dump(account)},HTTPStatus.CREATED

@accounts.put('/<string:code>')
@accounts.patch('/<string:code>')
def update(code):
    post_data = None
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {
            "error":"Post body JSON Data not found",
            "message":str(e)
        },HTTPStatus.BAD_REQUEST
    account = Account.query.filter_by(code=code).first()
    if(not account):
        return {
            "error":"Resource not found"
        }, HTTPStatus.NOT_FOUND
    account.observations = request.get_json().get("observations",account.observations)
    account.balance = request.get_json().get("balance",account.balance)
    account.registered_phone = request.get_json().get("registered_phone",account.registered_phone)
    
    try:
        db.session.commit()
    except sqlalchemy.ext.IntegrityError as e:
        return {
            "error":"Invalid update",
            "message":str(e)
        },HTTPStatus.BAD_REQUEST
    return {"data":account_schema.dump(account)},HTTPStatus.OK

@accounts.delete("/<string:code>")
def delete(code):
    account = Account.query.filter_by(code=code).first()
    if(not account):
        return {
            "error":"Resource not found"
        }, HTTPStatus.NOT_FOUND
    try:
        db.session.delete(account)
        db.session.commit()
    except sqlalchemy.ext.IntegrityError as e:
        return {
            "error":"Resource could not be deleted",
            "message":str(e)
        },HTTPStatus.BAD_REQUEST
    return {"data":""},HTTPStatus.NO_CONTENT
