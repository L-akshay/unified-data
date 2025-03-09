class DataSourceRouter:
    """
    A router to control all database operations on models for different
    data sources.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read from the specific database.
        """
        if hasattr(model, '_meta') and hasattr(model._meta, 'db_name'):
            return model._meta.db_name
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write to the specific database.
        """
        if hasattr(model, '_meta') and hasattr(model._meta, 'db_name'):
            return model._meta.db_name
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the same database.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure core app models only appear in the 'default' database.
        """
        if app_label == 'core':
            return db == 'default'
        return None
