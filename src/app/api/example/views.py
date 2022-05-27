"""Views."""
import json
import os
import uuid
import datetime

from flask import Blueprint, request, send_file
from flask.views import MethodView
from sqlalchemy.sql import select, desc

from ..support import responce
from ...tools.flasgger_marshmallow import swagger_decorator
from ...tools.odf_gen.content_modify import fill_template

example_blueprint = Blueprint('Example', __name__)
blueprint_name = example_blueprint.name
ROOT_PATH = os.path.dirname(__file__)


class CreateDocument(MethodView):
    """Создание документа."""

    @swagger_decorator(response_schema=responce(), blueprint_name=blueprint_name)
    def post(self):
        file_name = request.form['template_name']

        if file_name != '':
            if len(file_name.split('.')) == 1:
                file_name += '.odt'
            temp_file = 'templates/temp_odt/' + file_name
            if not os.path.exists(temp_file):
                return {'msg': 'Шаблона с таким именем нет.'}

            pdf_type = True if request.form.get('pdf_type') else False
            jd = request.form['json_data']
            if jd == '':
                jd = '{}'
            data = json.loads(jd.replace("'", '"'))

            result_file = 'doc_files/result_' + file_name

            length_file_name = len(file_name)
            pdf_file_name = 'result_' + file_name[:length_file_name -3] + 'pdf'

            open_doc = fill_template(os.path.join(ROOT_PATH, temp_file), data)

            try:
                open_doc.save(outputfile=result_file)
            except Exception as ex:
                print('сохранено с повреждениями')

            # command1 = f'libreoffice --headless --convert-to pdf {result_file}'
            command1 = 'unoconv -f pdf {}'.format(result_file)
            command2 = 'mv {} doc_files/'.format(pdf_file_name)

            import subprocess
            try:
                subprocess.check_call(['/usr/bin/python3', '/usr/bin/unoconv', '-f', 'pdf', result_file])
            except subprocess.CalledProcessError as e:
                print('SubProccess Error', e)

            os.system(command2)

            if pdf_type:
                try:
                    return send_file('doc_files/' + pdf_file_name, as_attachment=False)
                except Exception as ex:
                    return {"msg": "нет файла {}".format(pdf_file_name)}
            else:
                return send_file(result_file, as_attachment=False)
        else:
            return 'укажите имя шаблона *.odt'


class UploadTemplate(MethodView):

    @swagger_decorator(response_schema=responce(), blueprint_name=blueprint_name)
    def post(self):
        file = request.files['doc_file']

        if file.filename[-4:] != '.odt':
            return {"msg": 'неизвестный формат файла.'}

        if file.filename != '':
            in_filename = 'templates/temp_odt/' + file.filename
            file.save(in_filename)

        return {"msg": "upload template complete"}


example_blueprint.add_url_rule('/create_document', view_func=CreateDocument.as_view("createdocument_api"))
example_blueprint.add_url_rule('/put_template', view_func=UploadTemplate.as_view('uploadtemplate_api'))
