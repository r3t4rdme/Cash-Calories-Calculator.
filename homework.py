import datetime as dt


class Record:
    def __init__(self, amount: int, comment: str, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            this_date = dt.datetime.now().date()
            self.date = this_date
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_today_stats(self):
        today_summary = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                today_summary += record.amount
        return today_summary

    def get_week_stats(self):
        week_summary = 0
        week_ago = dt.datetime.now().date() - dt.timedelta(days=7)
        for record in self.records:
            if week_ago <= record.date <= dt.datetime.now().date():
                week_summary += record.amount
        return week_summary


class CashCalculator(Calculator):

    USD_RATE = 75.25
    EURO_RATE = 90.15

    def get_today_cash_remained(self, currency):
        cur_output = 0
        cur_name = ''
        remained_cash = self.limit - self.get_today_stats()
        if remained_cash == 0:
            return 'Денег нет, держись'
        elif currency == 'rub':
            cur_output = abs(remained_cash)
            cur_name = 'руб'
        elif currency == 'usd':
            cur_output = "%.2f" % (abs(float(remained_cash) / self.USD_RATE))
            cur_name = 'USD'
        elif currency == 'eur':
            cur_output = "%.2f" % (abs(float(remained_cash) / self.EURO_RATE))
            cur_name = 'Euro'
        if remained_cash > 0:
            return f'На сегодня осталось {cur_output} {cur_name}'
        else:
            return 'Денег нет, держись: твой долг - ' \
                    f'{cur_output} {cur_name}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_calories = self.get_week_stats()
        remained_calories = self.limit - today_calories
        if remained_calories > 0:
            return 'Сегодня можно съесть что-нибудь ещё,' \
                f' но с общей калорийностью не более {remained_calories} кКал'
        elif remained_calories <= 0:
            return 'Хватит есть!'
