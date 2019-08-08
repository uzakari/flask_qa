from flask.views import MethodView
from flask import Blueprint, jsonify, request

apis = Blueprint('apis', __name__)


languages = [{'name': 'python'}, {'name': 'javascript'},
             {'name': 'ruby'}, {'name': 'aspx.net'}]


def get_language(name):
    return [lang for lang in languages if lang['name'] == name][0]


class Language(MethodView):
    def get(self, language_name):
        try:
            if language_name:
                return jsonify({'language': get_language(language_name)})

            else:
                return jsonify({'language': languages})
        except:
            return jsonify({'language': 'An exception occured'})

    def post(self):
        try:
            new_lang_name = request.json['name']
            language = {'name': new_lang_name}
            languages.append(language)
            return jsonify({'language': get_language(new_lang_name)}), 201

        except:
            return jsonify({'exception': 'An exception has occured'}), 500

    def put(self, language_name):
        pass

    def delete(self, language_name):
        pass


language_view = Language.as_view('language_api')
apis.add_url_rule('/language', methods=['POST'], view_func=language_view)
apis.add_url_rule(
    '/language', methods=['GET'], defaults={'language_name': None}, view_func=language_view)
apis.add_url_rule('/language/<language_name>',
                  methods=['GET', 'PUT', 'DELETE'], view_func=language_view)
