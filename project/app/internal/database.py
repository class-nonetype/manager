import sqlalchemy.orm
import sqlalchemy

from app.utils import (log, DATABASE_URL)


# Crea un motor SQLAlchemy con la URL de la base de datos de AWS RDS y opciones de conexión.
engine = sqlalchemy.create_engine(url=DATABASE_URL)
log.debug('%s' % engine)

# Construye un generador de sesiones SQLAlchemy con configuraciones específicas.
#   - autocommit      Desactiva la confirmación automática de transacciones.
#   - autoflush       Desactiva la actualización automática de objetos en la sesión.
#   - bind            Asocia el motor creado anteriormente con las sesiones.
session = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Construye una clase base para definiciones de clases declarativas.
Base = sqlalchemy.orm.declarative_base()

