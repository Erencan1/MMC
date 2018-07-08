# MMC
Database Router to configure and switch databases in a live system for Django models


    The MMC wrapper is used to make Django database operations for the specified database, and switch that with another database in live system.
        ~ No need to set Router (https://docs.djangoproject.com/en/2.0/topics/db/multi-db/#no-cross-database-relations)
        ~ No need MyModel.objects.using(database_name)
    
    Here is how it is used:

```python
@MMC.setdb('DB2')
class Person(models.Model):
    name = models.CharField(max_length=30)
```

    p = Person.objects.first()
    p.name, p.save(), Person.objects.filter(), ... -> won't hit the default database but they will hit DB2!
    This is valid for all Django ORM queries.

    MMC also allows databases to switch in the live system.
```python
def switch_db(otherDB='DB3'):
    # from this point, all queries for Person Model will be using otherDB
    # If server/system is reloaded, it will revert to the initial settings.
    MMC.setdb(otherDB)(Person)
```
    
    MMC default methods: 
        @MMC.setdb(databaseName, methods=[save', 'delete', 'refresh_from_db', 'save_base',])
    
    # using(db)
```python
  p1 = Person.objects.last()    # will get the last object from database 'DB2'
  p2 = Person.objects.using('NEWDB').last() # will get the last object from database 'NEWDB'
  p3 = Person.objects.first()   # will get the first object from database 'DB2' again.
```

# MMC Wrapper

```python

class MMC:
    @classmethod
    def setdb(cls, db, methods=None):
        if methods is None or type(methods) is not list:
            methods = [
                'save',
                'delete',
                'refresh_from_db',
                'save_base',
            ]

        def set_db(the_class):

            the_class._mmc_db_name = db
            for method in methods:
                cls._add_using(the_class, method)

            the_class.objects = the_class.objects.using(db)
            return the_class

        return set_db

    @staticmethod
    def _add_using(the_class, method):
        fun = getattr(the_class, method)

        def mfun(*args, **kwargs):
            kwargs['using'] = the_class._mmc_db_name
            return fun(*args, **kwargs)

        setattr(the_class, method, mfun)

```
