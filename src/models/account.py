from datetime import datetime
from src.database import db,ma
from sqlalchemy import ForeignKey
from src.models import user

#Zona Modelo
class Account(db.Model):
    code = db.Column(db.String(5),primary_key=True)
    observations = db.Column(db.Text,nullable=True)
    balance = db.Column(db.Float,nullable=True)
    registered_phone = db.Column(db.String(10),nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    user_id = db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)

    def __init__(self,**fields):#Constructor, reciben muchos parametros
        super().__init__(**fields)
    
    def __repr__(self) -> str:#Similar a toString()
        return f"Account >>> {self.observations}"

#Zona Esquemas
class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Account
        include_fk = True

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
    