class CeleryRouter(object):
    

    # Define the applications to be used in the celery database
    APPS = (
        'django',
        'djcelery',
        'celery_haystack'
    )

    # Define Database Alias
    DB = 'celery'

    def db_for_read(self, model, **hints):
        """
        Point read operations to celery database.
        """
        if model._meta.app_label in self.APPS:
            return self.DB
        return None

    def db_for_write(self, model, **hints):
        """
        Point write operations to celery database.
        """
        if model._meta.app_label in self.APPS:
            return self.DB
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow any relation between two objects in the db pool
        """
        if (obj1._meta.app_label is self.APPS) and \
           (obj2._meta.app_label in self.APPS):
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the celery tables appear only in celery
        database.
        """
        if db == self.DB:
            return model._meta.app_label in self.APPS
        elif model._meta.app_label in self.APPS:
            return False
        return None