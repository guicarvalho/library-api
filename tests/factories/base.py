from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory
from factory import base
from faker import Faker

from tests.factories.factory_session_state import get_factory_session

fake = Faker()


class SQLAlchemyOptions(base.FactoryOptions):
    def _build_default_options(self):
        session = get_factory_session()
        return super()._build_default_options() + [
            base.OptionDefault("sqlalchemy_get_or_create", (), inherit=True),
            base.OptionDefault("sqlalchemy_session", session, inherit=False),
            base.OptionDefault(
                "sqlalchemy_session_factory",
                None,
                inherit=False,
            ),
            base.OptionDefault(
                "sqlalchemy_session_persistence",
                "commit",
                inherit=False,
            ),
        ]


class BaseModelFactory(AsyncSQLAlchemyFactory):
    _options_class = SQLAlchemyOptions

    class Meta:
        abstract = True
