import pymongo
import tools
import plot_tools
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

    return appear_per_day


def plot_appearances(name_list, end_date):

    start_date = date(2018, 1, 7)
    # e_date = date(2018, 1, 23)
    list_of_ap = list()

    date_range_list = list(tools.date_range(s_date, e_date + timedelta(days=1)))

    for idx, in_name in enumerate(name_list):
        list_of_ap.append(count_entity_articles(start_date, end_date, in_name))
        plot_tools.draw_entities_plot(in_name, list_of_ap[idx], date_range_list, "Article Appearances")


if __name__ == "__main__":
    s_date = date(2018, 1, 7)
    e_date = date(2018, 1, 31)
    # names = ["Theresa May", "Boris Johnson", "Jeremy Corbyn", "David Davis", "Donald Trump", "Nigel Farage"]
    names = ["Carillion", "NHS", "Labour", "Tory"]
    # names = ["EU", "UK", "US", "UN"]

    plot_appearances(names, e_date)
