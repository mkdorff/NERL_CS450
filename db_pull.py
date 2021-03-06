import ignore
import pickle
from peewee import *

db = MySQLDatabase('Wikilinks', user='root', passwd=ignore.password_string, charset='utf8mb4')

class LongTextField(TextField):
    db_field = 'longtext'

class Page(Model):
    title = CharField()
    links = LongTextField()

    class Meta:
        database = db

db.connect()
# db.create_tables([Page])
# AFTER creation, go to my sql work bench and change links to utf8mb4

nodes = {}
max_id = Page.select(fn.MAX(Page.id)).scalar()
print(max_id)


#       1- 500000
#  500001-1000000
# 1000001-1500000
# 1500001-2000000
# 2000001-2500000
# 2500001-3000000
# 3000001-3500000
# 3500001-4000000
# 4000001-4500000
# 4500001-5000000
# 5000001-5538056


for x in range(max_id):
    current_page = Page.select().where(Page.id == x+1).get()
    current_links = current_page.links.split("###")

    for node in current_links:
        if node in nodes:
            nodes[node] += 1
        else:
            nodes[node] = 1

    if not x % 10000:
        print(x)

with open('nodes_01.pickle', 'wb') as handle:
    pickle.dump(nodes, handle, protocol=pickle.HIGHEST_PROTOCOL)


# print(list(range(1,51)))