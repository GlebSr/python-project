from models import Product
from database import MongoDB
class Product_repository:
    db: MongoDB
    def add(self, product: Product):
        product_data = product.to_dict
        result = self.db.db["products"].insert_one(product_data)
        return result