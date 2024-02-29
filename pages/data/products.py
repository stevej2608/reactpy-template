
from typing import List
from pydantic import BaseModel
from reactpy_table import ColumnDef, Columns
from utils.make_data import make_data

PRODUCTS = [
    {"name": "Education Dashboard", "description": "Html templates", "technology": "Angular", "id": "#194556", "price": "$149"},
    {"name": "React UI Kit", "description": "Html templates", "technology": "React JS", "id": "#623232", "price": "$129"},
    {"name": "DashboardPro", "description": "Html templates", "technology": "SolidJS", "id": "#194334", "price": "$449"},
    {"name": "Charts Package", "description": "Fancy charts", "technology": "Angular", "id": "#323323", "price": "$129"},
    {"name": "Server Render", "description": "NodeJS", "technology": "Typescript", "id": "#994336", "price": "$749"},
    {"name": "Accounts Package", "description": "NodeJS", "technology": "Typescript", "id": "#144256", "price": "$779"},
    {"name": "Grav CMS", "description": "Content Management", "technology": "PHP", "id": "#624478", "price": "$29"},
    {"name": "Wordpress", "description": "Content Management", "technology": "PHP", "id": "#192656", "price": "$55"}
]

COLS: Columns = [
    ColumnDef(name='index', label='#'),
    ColumnDef(name='name', label='Name'),
    ColumnDef(name='description', label='Description'),
    ColumnDef(name='technology', label='Technology'),
    ColumnDef(name='id', label='ID'),
    ColumnDef(name='price', label='Price')
    ]

class Product(BaseModel):
    index: int
    name: str
    description: str
    technology: str
    id: str
    price: str

def make_products(number: int) -> List[Product] :
    return make_data(number, PRODUCTS, Product)
