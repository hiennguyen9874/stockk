# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.industry import Industry  # noqa
from app.models.item import Item  # noqa
from app.models.ticker import Ticker  # noqa
from app.models.user import User  # noqa
