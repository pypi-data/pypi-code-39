import sqlalchemy
from sqlalchemy_utils import database_exists, create_database

from daopy import model, utils


# ------------------------------------------------------------------------------
class AbstractBaseDao:
    """
    Abstract base DAO class for extension by concrete DAO classes.
    """

    def __init__(self, database_config, model_class):
        """
        Constructor function.

        :param database_config:
        """

        # create an engine from the configuration parameters
        if utils.config_has_section(database_config, "SQLITE"):

            params = utils.parse_config(database_config, section="SQLITE")
            engine = sqlalchemy.create_engine(f"sqlite:///{params['sqlite_file']}",
                                              connect_args={"check_same_thread": False},
                                              echo=True)

        elif utils.config_has_section(database_config, "POSTGRESQL"):

            params = utils.parse_config(database_config, section="POSTGRESQL")
            connection_details = f"postgresql+psycopg2://{params['user']}:" + \
                                 f"{params['password']}@{params['host']}:" + \
                                 f"{params['port']}/{params['database']}"
            engine = sqlalchemy.create_engine(connection_details, echo=True)

        else:

            message = f"Invalid database configuration file: {database_config}"
            raise ValueError(message)

        # build the database if not present
        if not database_exists(engine.url):
            create_database(engine.url)

        # create all tables, etc.
        model_class.metadata.create_all(engine)

        # establish the session
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        self.session = Session()

        # the class of the model type we're using the DAO for access
        self.model_class = model_class

    def insert(self, item):
        """
        Inserts a single item.

        :param item:
        :return:
        """
        item = self.session.add(item)
        self.session.commit()
        return item

    def insert_all(self, items):
        """
        Inserts a collection of items.

        :param list items:
        :return:
        """

        self.session.bulk_save_objects(items)
        self.session.commit()

    def update(self, object_id, attribute_values):
        """
        Updates a single item identified by the provided key by assigning
        the provided value to the item's named attributes.

        :param object_id: primary key ID of the item that will be updated
        :param dict attribute_values: name/value pairs of the attributes that
            are being updated for the referenced item
        :return:
        """

        item = self.session.query(self.model_class).filter(self.model_class.id == object_id)
        item.update(attribute_values, synchronize_session="fetch")
        self.session.commit()

    def delete(self, object_id):
        """
        Deletes a single item identified by the provided key.

        :param object_id: primary key ID of the item that will be deleted
        :return:
        """

        item = self.session.query(self.model_class).filter(self.model_class.id == object_id)
        item.delete(synchronize_session="fetch")
        self.session.commit()

    def find(self, object_id):
        """
        Finds a single item based on the provided key. If the item doesn't exist
        then None is returned.

        :param object_id:
        :return: the item identified by `object_id`, or None if it doesn't exist
        """

        item = self.session.query(self.model_class).get(object_id)
        return item


# ------------------------------------------------------------------------------
class DetectionDao(AbstractBaseDao):
    """
    DAO class for detection objects.
    """

    def __init__(self, database_config):
        """
        Constructor

        :param database_config: configuration file containing Postrgres database
            connection properties
        """

        # invoke the base class constructor
        super().__init__(database_config, model.Detection)
