#! /usr/bin/python3
# coding: utf8

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, SubmitField, FieldList, FormField, DecimalField, validators, FileField
from lxml.builder import E
from lxml import etree
from werkzeug import secure_filename

server = Flask(__name__)
server.config['SECRET_KEY'] = 'secretkey'


class TestForm(FlaskForm):
    test_type = SelectField('Type', [validators.DataRequired()], choices=[('assert', 'Assert'), ('script', 'Script'), ('motif', 'Motif')], default='assert')
    test_assert_function = TextField("Fonction")
    test_motif = TextField("Motif")
    test_assert_result = TextField("Résultat")
    test_points = DecimalField("Points", [validators.DataRequired()])
    test_script = FileField("Script")

    def toXml(self):
        root = E.test()
        if self.test_type.data == 'assert':
            root = E.test(
                E.type(self.test_type.data),
                E.function(self.test_assert_function.data),
                E.result(self.test_assert_result.data),
                E.points(str(self.test_points.data))
            )

        if self.test_type.data == 'script':
            root = E.test(
                E.type(self.test_type.data),
                E.file(self.test_script.data.filename)
            )

        if self.test_type.data == 'motif':
            root = E.test(
                E.type(self.test_type.data),
                E.motif(self.test_motif.data),
                E.points(str(self.test_points.data))
            )

        return root


class FullForm(FlaskForm):
    langage = SelectField('Langage', [validators.DataRequired()], choices=[('java', 'Java'), ('c', 'C')])
    commande_compil = TextField('Commande de compilation', [validators.DataRequired()])
    points = DecimalField('Points', [validators.DataRequired()])
    tests = FieldList(FormField(TestForm), min_entries=1)
    submit = SubmitField('Submit')

    def toXml(self):
        root = E.tp(
            E.langage(self.langage.data),
            E.compilation(
                E.command(self.commande_compil.data),
                E.point(str(self.points.data))),
        )
        cpt = 1
        for elem in self.tests:
            root.append(elem.toXml())
            cpt += 1
        return root


@server.route('/')
def home():
    form = FullForm()
    return render_template('test.html', form=form)


@server.route('/import', methods=['POST'])
def upload():
    form = FullForm()
    print(form.validate_on_submit())
    print(form.errors)
    result = ""
    if form.validate_on_submit():
        for elem in form.tests:
            if elem.test_type.data == 'script':
                if elem.test_script.data != "":
                    filename = secure_filename(elem.test_script.data.filename)
                    elem.test_script.data.save("/tmp/" + filename)
                else:
                    return render_template('test.html', form=form, error="file required")

        root = form.toXml()

        result = etree.tostring(root,
                                xml_declaration=True,
                                encoding='utf8',
                                pretty_print=True).decode('utf-8')
        return render_template('result.html', result=result)
    else:
        return render_template('test.html', form=form, error=form.errors)


if __name__ == '__main__':
    server.run("0.0.0.0", debug=True)
