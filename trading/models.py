from typing import List, Optional

from sqlalchemy.dialects.postgresql import UUID

from trading import db


class BaseModel(db.Model):
    def to_dict(self, show: Optional[List[str]] = None, hide: List[str] = []):
        """
        Transform model into dict

        Params:
            show: columns to show
            hide: columns to hide
        """

        if show is None:
            return {
                str(each.name): getattr(self, each.name)
                for each in self.__table__.columns
                if each.name not in hide
            }
        else:
            return {
                str(each.name): getattr(self, each.name)
                for each in self.__table__.columns
                if each.name in show and each.name not in hide
            }


class TimeStampedModel(BaseModel):

    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
    )


class Account(TimeStampedModel):

    __tablename__ = "account"

    id = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    start_cash = db.Column(db.Integer)
    total_purchase = db.Column(db.Float, default=0)
    cash = db.Column(db.Integer)
    stock_count = db.Column(db.Integer, default=0)


class Order(TimeStampedModel):

    __tablename__ = "order"

    id = db.Column(UUID, primary_key=True)
    account_id = db.Column(UUID, db.ForeignKey("account.id"))
    code = db.Column(db.String(6))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    side = db.Column(db.String)
    unfilled = db.Column(db.Integer)
