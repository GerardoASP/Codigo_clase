from datetime import datetime
from src.database import db,ma

class Product(db.Model): #dios mio
    code = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50),unique=True)
    price = db.Column(db.Float,nullable=False)
    expiration = db.Column(db.DateTime,nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    user_id = db.Column(db.String(10),db.ForeignKey('user.id',onupdate="CASCADE",ondelete="RESTRICT"),nullable=False)
    
    def __init__(self,**fields):#Constructor, reciben muchos parametros
        super().__init__(**fields)
    
    def __repr__(self) -> str:#Similar a toString()
        return f"Product >>> {self.name}"
    
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        #fields
        model = Product
        include_fk = True

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)