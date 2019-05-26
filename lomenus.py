from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item

engine = create_engine('sqlite:///plants.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


category1 = Category(name="Plantas Terrestres")

session.add(category1)
session.commit()

Item1 = Item(name="Musgos", description="Descriçao legal de musgos pois eles sao muito bons",
                      category=category1)

session.add(Item1)
session.commit()

Item2 = Item(name="Arbustos", description="Otimos pra fazer uma pequena sombrinha",
                      category=category1)

session.add(Item2)
session.commit()


category2 = Category(name="Plantas Aquaticas")

session.add(category2)
session.commit()

Item3 = Item(name="Vitoria-Regia", description="Sempre lembra sapos",
                      category=category2)

session.add(Item3)
session.commit()

Item4 = Item(name="Lotus", description="Uma maquina de corrida?",
                      category=category2)

session.add(Item4)
session.commit()


category3 = Category(name="Plantas Aereas")

session.add(category3)
session.commit()

Item5 = Item(name="filodendro", description="NUnca ouvi falar",
                      category=category3)

session.add(Item5)
session.commit()

Item6 = Item(name="costela de adao", description="opa, bao ein!?",
                      category=category3)

session.add(Item6)
session.commit()


category4 = Category(name="Plantas de Jardim")

session.add(category4)
session.commit()

Item7 = Item(name="Bromelia:", description="Das antigas",
                      category=category4)

session.add(Item7)
session.commit()

Item8 = Item(name="Violeta", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category4)

session.add(Item8)
session.commit()

print("added menu items!")
