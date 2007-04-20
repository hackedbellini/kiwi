import datetime

import gtk

from sqlobject import connectionForURI, SQLObject, StringCol, DateCol, DecimalCol
from kiwi.datatypes import currency
from kiwi.db.sqlobj import SQLObjectQueryExecuter
from kiwi.ui.objectlist import Column
from kiwi.ui.search import SearchSlaveDelegate, DateSearchFilter

__connection__ = conn = connectionForURI('sqlite:///:memory:')

class Sale(SQLObject):
    description = StringCol()
    price = DecimalCol(size=10, precision=2)
    date = DateCol()
Sale.createTable(ifNotExists=True)

if Sale.select().count() == 0:
    today = datetime.date.today()
    for description, price, date in [
        ('Cup of coffee', 2.04, today - datetime.timedelta(1)),
        ('Chocolate bar', 1.85, today - datetime.timedelta(40)),
        ('Candy',         0.99, today - datetime.timedelta(30)),
        ('Grape Juice',   3.38, today - datetime.timedelta(23)),
        ('Ice tea',       1.25, today - datetime.timedelta(10)),
        ('Cookies',       0.85, today - datetime.timedelta(5)),
        ('Noogies',       1.45, today - datetime.timedelta(2)),
        ('Nuts',          2.95, today)]:
        Sale(description=description,
             price=price,
             date=date)

class BirthdayViewer(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.search = SearchSlaveDelegate(self.get_columns())
        self.add(self.search.get_toplevel())
        self._setup_searching()
        self._create_filters()

    def _setup_searching(self):
        self.query = SQLObjectQueryExecuter(conn)
        self.search.set_query_executer(self.query)
        self.query.set_table(Sale)


    def _create_filters(self):
        self.query.set_filter_columns(self.search.get_primary_filter(),
                                      ['description'])

        date_filter = DateSearchFilter('Date:')
        self.query.set_filter_columns(date_filter, ['date'])
        self.search.add_filter(date_filter)

    def get_columns(self):
        return [Column('description', expand=True, title='Description'),
                Column('price', data_type=currency,
                       expand=True, title='Description'),
                Column('date', data_type=datetime.date,
                       title='Birthdate')]


view = BirthdayViewer()
view.set_size_request(-1, 400)
view.connect('delete-event', gtk.main_quit)
view.show_all()
gtk.main()