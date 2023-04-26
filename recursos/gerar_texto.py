from flask_restful import Resource
from auxiliary_functions.tratar_texto import GenerateText
from auxiliary_functions.cron import ValidarCron


class Text(Resource):

    def get(self, language, cron):
        value_aux = ValidarCron(cron)


        if 'message' in value_aux.validator_cron().keys():
            return value_aux.validator_cron(), 404
            

        value = GenerateText(cron)
        value_api =  {'minute': value.text_minute().replace('At ', '').strip()
                ,'hour': value.text_hour().replace('past ', '').strip()
                ,'day': value.text_day().replace('on ', '').strip()
                ,'month': value.text_month().replace('in ', '').strip()
                ,'week': value.text_day_week().replace('on ', '').strip()
                ,'full': (value.text_minute() 
                            + value.text_hour() 
                            + value.text_day() 
                            + value.text_day_week() 
                            + value.text_month())
                }
        if language.lower() == 'en':
            return value_api,200
        return GenerateText.translator(value_api, language), 200
    