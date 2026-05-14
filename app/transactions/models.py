from datetime import datetime, timezone

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    title = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False, default="")
    transaction_date = db.Column(db.Date, nullable=True, index=True)
    transaction_hour = db.Column(db.Time, nullable=True)
    is_recurring = db.Column(db.Boolean, default=False, nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    interval = db.Column(db.String(255), nullable=True)
    number_of_payments = db.Column(db.Integer, nullable=True)
    transaction_type = db.Column(db.String(32), nullable=False, index=True)

    user = db.relationship("User", back_populates="transactions")

    def to_dict(self) -> dict:
        return {
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "title": self.title,
            "amount": float(self.amount),
            "category": self.category,
            "payment_method": self.payment_method,
            "description": self.description,
            "transaction_date": (
                self.transaction_date.isoformat()
                if self.transaction_date
                else ""
            ),
            "transaction_hour": (
                self.transaction_hour.strftime("%H:%M")
                if self.transaction_hour
                else ""
            ),
            "is_recurring": self.is_recurring,
            "start_date": self.start_date.isoformat() if self.start_date else "",
            "end_date": self.end_date.isoformat() if self.end_date else "",
            "interval": self.interval,
            "number_of_payments": self.number_of_payments,
            "transaction_type": self.transaction_type,
        }
