from auxiliary_functions.cron import TratarCron, ValidarCron
# from translate import Translator
from googletrans import Translator
import re
from math import ceil


class GenerateText():

    def __init__(self, cron):
        

        self.cron = cron

    def name_month(text):
        months = {
            '1': 'January'
            ,'2': 'February'
            ,'3': 'March'
            ,'4': 'April'
            ,'5': 'May'
            ,'6': 'June'
            ,'7': 'July'
            ,'8': 'August'
            ,'9': 'September'
            ,'10': 'October'
            ,'11': 'November'
            ,'12': 'December'
        }

        list_months = ValidarCron.get_numbers(text)

        for x in list_months:
            text = text.replace(str(x), months[str(x)])
        return text

    def name_day_week(text):
        day_week = {
            '0': 'Sunday'
             ,'1': 'Monday'
             ,'2': 'Tuesday'
             ,'3': 'Wednesday'
             ,'4': 'Thursday'
             ,'5': 'Friday'
             ,'6': 'Saturday'
        }

        list_months = ValidarCron.get_numbers(text)

        for x in list_months:
            text = text.replace(str(x), day_week[str(x)])
        return text

    def normalize_month_day_week_in_text(text):
        text = text.replace('  ', ' ')
        if 'month' in text:
            replace_text = 'month'
        elif 'day-of-week' in text:
            replace_text = 'day-of-week'
        else: 
            return text
        
        text_aux = text.replace(replace_text, '')
        text_aux = text_aux.replace('  ', ' ')
        return text_aux.replace('every from', f'every {replace_text} from')

    def normalize_text(text, replace_text):
        value = text.replace(replace_text, '')
        value_list = value.split(',')
        if 'every' in value_list[0]:
            return f'{value.strip()} {replace_text}'
        elif value_list[0] == '*':
            return f'every {replace_text}'
        
        new_list_text = []

        if ' and ' in value_list[0]:
            value_list_aux = value_list[0].split(' and ')

            for x in value_list_aux:
                if 'through' not in x:
                    text_aux = x.strip()
                    new_list_text.append(f'{replace_text} {text_aux}')
                else:
                    text_aux = x.strip()
                    new_list_text.append(f'every{replace_text} from {text_aux}')

            return ' and '.join(new_list_text)
        
        
        elif len(value_list) == 1:
            text_aux = value_list[0].strip()
            if 'through' not in value_list[0]:
                return f'{replace_text} {text_aux}'
            else:
                return f'every{replace_text} from {text_aux}'
        
        elif 'through' not in value_list[0]:
            text_aux = value_list[0].strip()
            new_list_text.append(f'{replace_text} {text_aux}')
        else:
            text_aux = value_list[0].strip()
            new_list_text.append(f'every{replace_text} from {text_aux}')

        try:
            for x in value_list[1:-1]:
                if ' and ' in x:
                    pass            
                elif 'through' not in x:
                    text_aux = x.strip()
                    new_list_text.append(text_aux)
                else:
                    text_aux = x.strip()
                    new_list_text.append(f'every{replace_text} from {text_aux}')

            value_list = value_list[-1].split(' and ')
            new_list_text_2 = []
            for x in value_list:
                if 'through' not in x:
                    text_aux = x.strip()
                    new_list_text_2.append(text_aux)
                else:
                    text_aux = x.strip()
                    new_list_text_2.append(f'every{replace_text} from {text_aux}')

            new_list_text_2 = ' and '.join(new_list_text_2)
            new_list_text.append(new_list_text_2)
            return ', '.join(new_list_text)
        except:
            return ', '.join(new_list_text)

    def criterion(self):
        value = ValidarCron(self.cron)
        if 'message' in value.validator_cron().keys():
            return None
        return value.validator_cron()
    
    def text_minute(self):
        value = GenerateText(self.cron)
        value = value.criterion()
        if value:
            body = 'At {text} '
            text = TratarCron(**value).tratar_minute()
            text = GenerateText.normalize_text(text, ' minute')
            return body.replace('{text}', text).replace('  ',' ')
            
        text = ValidarCron(self.cron)
        return text.validator_cron().replace('  ',' ')
    
    def text_hour(self):
        value = GenerateText(self.cron)
        value = value.criterion()
        if value:
            body = 'past {text} '
            text = TratarCron(**value).tratar_hour()
            text = GenerateText.normalize_text(text, ' hour')
            return body.replace('{text}', text).replace('  ',' ')
            
        text = ValidarCron(self.cron)
        return text.validator_cron().replace('  ',' ')
    
    def text_day(self):
        value = GenerateText(self.cron)
        value = value.criterion()
        if value:
            body = 'on {text} '
            text = TratarCron(**value).tratar_day()
            text = GenerateText.normalize_text(text, ' day-of-month')
            return body.replace('{text}', text).replace('  ',' ')
            
        text = ValidarCron(self.cron)
        return text.validator_cron().replace('  ',' ')
    
    def text_month(self):
        value = GenerateText(self.cron)
        value = value.criterion()
        if value:
            body = 'in {text} '
            text = TratarCron(**value).tratar_month()
            text = GenerateText.normalize_text(text, ' month')
            text = body.replace('{text}', text).replace('  ',' ')
            text = GenerateText.normalize_month_day_week_in_text(text)
            return GenerateText.name_month(text)
            
        text = ValidarCron(self.cron)
        return text.validator_cron().replace('  ',' ')
    
    def text_day_week(self):
        value = GenerateText(self.cron)
        value = value.criterion()
        if value:
            body = 'on {text} '
            text = TratarCron(**value).tratar_day_week()
            text = GenerateText.normalize_text(text, ' day-of-week')
            text = body.replace('{text}', text).replace('  ',' ')
            text = GenerateText.normalize_month_day_week_in_text(text)
            return GenerateText.name_day_week(text)
            
        text = ValidarCron(self.cron)
        return text.validator_cron().replace('  ',' ')
    
    def create_dict(dict_text):

        text = str(dict_text).replace("'", "").replace('{', '').replace('}','')

        padrao = r"\b\w+\b\s*:"
        matches = re.findall(padrao, text)

        dict_text = {}
        for x in range(1,len(matches)):
            end_text = text.find(matches[x])
            text_aux = text[:end_text]

            text = text[end_text:]

            text_aux = text_aux.replace(matches[x-1], '')
            key = matches[x-1].replace(':', '')
            dict_text[key] = text_aux

        text_aux = text.replace(matches[-1], '')
        key = matches[-1].replace(':', '')
        dict_text[key] = text_aux

        return dict_text

    def translator(text, language):
        text = str(text)
        
        # start = 0
        # end = len(text)
        # step = 500

        # list_text = []

        # for x in range(ceil(len(text)/500)):
        #     if start + step >= end:
        #         list_text.append(text[start:])
        #     else:
        #         list_text.append(text[start:start+step])

        #     start+= step
        
        # translator= Translator(to_lang=f"{language}") #aqui
        # for x in range(len(list_text)):
        #     list_text[x] = translator.translate(list_text[x])
        
        # text =  ''.join(list_text)

        tradutor = Translator()
        text = tradutor.translate(text, dest=f'{language}')

        return GenerateText.create_dict(text.text)