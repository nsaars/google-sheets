from sqlalchemy import sql, Column, Sequence, Integer, BigInteger, Date, Float
from db.database import db


class Order(db.Model):
    __tablename__ = "orders"
    query: sql.Select

    id = Column(BigInteger, Sequence("orders_id_seq"), primary_key=True)
    order_number = Column(BigInteger)
    price = Column(Integer)
    delivery_time = Column(Date)
    ruble_price = Column(Integer)

    def __repr__(self):
        return f"""
            Order: {self.id} - {self.price}
        """

