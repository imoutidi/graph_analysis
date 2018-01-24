import pymongo
import tools
import pickle
from datetime import date, timedelta


# Creates an index for the text field
# For all the collections of the database
def create_indexes():
    # Getting data from the mongo database
    client = pymongo.MongoClient()
    # Database name is minedNews
    db = client.minedArticles

    collection_names = db.collection_names()
    for name in collection_names:
        db[name].create_index([('text', pymongo.TEXT)], name='text_index', default_language='english')


def count_entity_articles(start_date, end_date, entity_name):
    # Getting data from the mongo database
    client = pymongo.MongoClient()
    # Database name is minedNews
    db = client.minedArticles
    query_entity = "\"" + entity_name + "\""
    date_range_list = list(tools.date_range(start_date, end_date + timedelta(days=1)))
    appear_per_day = list()

    for c_date in date_range_list:
        c_day = str(c_date.year) + "-" + str(c_date.month) + "-" + str(c_date.day)
        week = str(c_date.isocalendar()[1]) + "-" + str(c_date.isocalendar()[0])
        docs = db[week].find({"$and": [{"$text": {"$search": query_entity}}, {"date": c_day}]})
        # counting the elements of the generator
        appear_per_day.append(sum(1 for _ in docs))

    print(appear_per_day)
    return sum(appear_per_day)


def top_ten_stats():
    ser_entity_types = ["P", "L", "O", "LO", "PL", "PO", "PLO"]
    relation_types = ["Article", "Sentence", "Article_Sentence"]

    for entity_type in ser_entity_types:
        for relation_type in relation_types:
            load_metrics = open("/home/iraklis/PycharmProjects/graph_analysis/pickle_files/"
                                + relation_type + "_" + entity_type + "_dict.pickle", "rb")
            global_metrics_dict_list = pickle.dump(load_metrics)
            load_metrics.close()




    s_date = date(2018, 1, 7)
    e_date = date(2018, 1, 23)
    print(count_entity_articles(s_date, e_date, "Theresa May"))




