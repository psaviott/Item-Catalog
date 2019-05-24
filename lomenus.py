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


# Menu for UrbanBurger
category1 = Category(name="Plantas Terrestres")

session.add(category1)
session.commit()

menuItem1 = Item(name="Musgos", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category1)

session.add(menuItem1)
session.commit()

menuItem2 = Item(name="Arbustos", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category1)

session.add(menuItem2)
session.commit()


category2 = Category(name="Plantas Aquaticas")

session.add(category2)
session.commit()

menuItem3 = Item(name="Teste 2", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category2)

session.add(menuItem3)
session.commit()

menuItem4 = Item(name="Teste 3", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category2)

session.add(menuItem4)
session.commit()


category3 = Category(name="Plantas Aereas")

session.add(category3)
session.commit()

menuItem5 = Item(name="Teste 5", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category3)

session.add(menuItem5)
session.commit()

menuItem6 = Item(name="Teste 6", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category3)

session.add(menuItem6)
session.commit()


category4 = Category(name="Plantas de Jardim")

session.add(category4)
session.commit()

menuItem7 = Item(name="Teste 7", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category4)

session.add(menuItem7)
session.commit()

menuItem8 = Item(name="Teste 8", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                      category=category4)

session.add(menuItem8)
session.commit()

print("added menu items!")
