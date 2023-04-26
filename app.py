from translate import Translator
from flask import Flask
from flask_restful import Api
from recursos.gerar_texto import Text

# Minuto (0 - 59)
# Hora (0 - 23)
# Dia do mês (1 - 31)
# Mês (1 - 12)
# dia da semana (0 - 6)

app = Flask(__name__)
api = Api(app)

# api.add_resource(Text, '/cron/<string:cron>')
api.add_resource(Text, '/cron/<string:language>/<string:cron>')


if __name__ == '__main__':
    app.run(debug=True)