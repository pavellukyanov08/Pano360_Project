from sqlalchemy import create_engine

# Замените эту строку на вашу строку подключения
db_uri = 'postgresql://postgres:PavelDB@localhost:5440/pano360_db'
try:
    engine = create_engine(db_uri)
    connection = engine.connect()
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(e)
