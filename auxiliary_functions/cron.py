import re

class CronSeparador():

    def find_asterisk(valor):
        if '*' in valor:
            return valor
        return None
    
    def find_bar(valor):
        if '/' in valor:
            return valor
        return None

class TratarCron():

    def __init__(self, minute, hour, day, month, day_week):
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.day_week = day_week

    def tratar_asterisk_bar(valor):
        if CronSeparador.find_asterisk(valor):
            if CronSeparador.find_bar(valor):
                return 'every ' + valor.split('/')[-1] + ' {texto}'
            return 'all'
        return None
    
    def tratar_comma_hyphen(valor):
        texto = valor
        
        if len(valor.split(',')) > 1:
            sep_text = valor.split(',')
            texto = ' {texto}, '.join(sep_text[:-1]) + ' {texto}' + ' and ' + sep_text[-1] 
        
        if len(valor.split('-')) > 1:
            texto = texto.replace('-', ' {texto} through ')

        return texto + ' {texto}'

    def tratar_minute(self):
        if TratarCron.tratar_asterisk_bar(self.minute) == 'all':
            return 'every minute'
        elif TratarCron.tratar_asterisk_bar(self.minute):
            return TratarCron.tratar_asterisk_bar(self.minute).replace('{texto}', 'minute')
        return TratarCron.tratar_comma_hyphen(self.minute).replace('{texto}', 'minute')
    
    def tratar_hour(self):
        if TratarCron.tratar_asterisk_bar(self.hour) == 'all':
            return 'every hour'
        if TratarCron.tratar_asterisk_bar(self.hour):
            return TratarCron.tratar_asterisk_bar(self.hour).replace('{texto}', 'hour')
        return TratarCron.tratar_comma_hyphen(self.hour).replace('{texto}', 'hour')
    
    def tratar_day(self):
        if TratarCron.tratar_asterisk_bar(self.day) == 'all':
            return 'every day'
        if TratarCron.tratar_asterisk_bar(self.day):
            return TratarCron.tratar_asterisk_bar(self.day).replace('{texto}', 'day-of-month')
        return TratarCron.tratar_comma_hyphen(self.day).replace('{texto}', 'day-of-month')

    def tratar_month(self):
        if TratarCron.tratar_asterisk_bar(self.month) == 'all':
            return 'every month'
        if TratarCron.tratar_asterisk_bar(self.month):
            return TratarCron.tratar_asterisk_bar(self.month).replace('{texto}', 'month')
        return TratarCron.tratar_comma_hyphen(self.month).replace('{texto}', 'month')

    def tratar_day_week(self):
        if TratarCron.tratar_asterisk_bar(self.day_week) == 'all':
            return 'every day'
        if TratarCron.tratar_asterisk_bar(self.day_week):
            return TratarCron.tratar_asterisk_bar(self.day_week).replace('{texto}', 'day-of-week')
        return TratarCron.tratar_comma_hyphen(self.day_week).replace('{texto}', 'day-of-week')

class ValidarCron():

    def __init__(self, cron):
        self.cron = cron
    
    def list_cron(text):
        return text.split(' ')
    
    def get_numbers(text):
        expr = text
        numbers = re.findall(r'\d+', expr)
        return [int(number) for number in numbers]

    def validator_length_cron(self):
        value = len(self.cron.strip().split(' '))
        if value == 5:
            return self.cron
        return None
    
    def validator_minute(self):
        # Minute (0 - 59)
        value = ValidarCron.list_cron(self.cron)
        if '*' == value[0]:
            return self.cron
        number = ValidarCron.get_numbers(value[0])
        if min(number) >= 0 and max(number) <= 59:
            return self.cron
        return None

    def validator_hour(self):
        # Hour (0 - 23)
        value = ValidarCron.list_cron(self.cron)
        if '*' == value[1]:
            return self.cron
        number = ValidarCron.get_numbers(value[1])
        if min(number) >= 0 and max(number) <= 23:
            return self.cron
        return None
    
    def validator_day(self):
        # Day (1 - 31)
        value = ValidarCron.list_cron(self.cron)
        if '*' == value[2]:
            return self.cron
        number = ValidarCron.get_numbers(value[2])
        if min(number) >= 0 and max(number) <= 31:
            return self.cron
        return None
    
    def validator_month(self):
        # Month (1 - 12)
        value = ValidarCron.list_cron(self.cron)
        if '*' == value[3]:
            return self.cron
        number = ValidarCron.get_numbers(value[3])
        if min(number) >= 0 and max(number) <= 12:
            return self.cron
        return None
    
    def validator_day_week(self):
        # Day Week (0 - 6)
        value = ValidarCron.list_cron(self.cron)
        if '*' == value[4]:
            return self.cron
        number = ValidarCron.get_numbers(value[4])
        if min(number) >= 0 and max(number) <= 6:
            return self.cron
        return None
    
    def validator_cron(self):
        value = ValidarCron(self.cron)
        if value.validator_length_cron() is None:
            return {'message': 'invalid cron.'}
        elif value.validator_minute() is None:
            return {'message': 'invalid minute.'}
        elif value.validator_hour() is None:
            return {'message': 'invalid hour.'}
        elif value.validator_day() is None:
            return {'message': 'invalid day.'}
        elif value.validator_month() is None:
            return {'message': 'invalid month.'}
        elif value.validator_day_week() is None:
            return {'message': 'invalid day week.'}
        else:
            value = ValidarCron.list_cron(self.cron)
            return {
                    'minute': value[0],
                    'hour': value[1],
                    'day': value[2],
                    'month': value[3],
                    'day_week': value[4]
                    }