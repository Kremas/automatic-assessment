#! /usr/bin/python3
# coding: utf8

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, FieldList, FormField, TextField, DecimalField, FileField, SubmitField, validators, ValidationError
from lxml import etree
from lxml.builder import E


server = Flask(__name__)
server.config['SECRET_KEY'] = 'secretkey'


class Assert(FlaskForm):
    function = TextField("Fonction", [validators.DataRequired()])
    result = TextField("Résultat", [validators.DataRequired()])

    def toXml(self):
        root = (E.function(self.function.data), E.result(self.result.data))
        return root


class Motif(FlaskForm):
    motif = TextField('Motif', [validators.InputRequired()])


class Script(FlaskForm):
    script = FileField('Script', [validators.InputRequired()])


class TestForm(FlaskForm):
    test_type = SelectField('Type', [validators.InputRequired()], choices=[('assert', 'Assert'), ('script', 'Script'), ('motif', 'Motif')], default='assert')
    points = DecimalField("Points", [validators.InputRequired()])
    a = FormField(Assert)
    m = FormField(Motif)
    s = FormField(Script)

    def validate(self):
        FlaskForm.validate(self)
        print(self.errors)
        if 'points' in self.errors:
            return False
        if 'test_type' in self.errors:
            return False

        if 'a' not in self.errors or 'm' not in self.errors or 's' not in self.errors:
            return True

    def toXml(self):
        if self.test_type.data == 'assert':
            t = self.a.toXml()
        elif self.test_type.data == 'motif':
            t = self.m.toXml()
        else:
            t = self.s.toXml()

        root = E.test(E.type(self.test_type.data))
        for elem in t:
            root.append(elem)

        return root


class FullForm(FlaskForm):
    langage = SelectField('Langage', [validators.InputRequired()], choices=[('java', 'Java'), ('c', 'C'), ('python', 'Python')])
    tests = FieldList(FormField(TestForm), min_entries=1)
    submit = SubmitField()

    def toXml(self):
        root = E.tp(
            E.langage(self.langage.data),
        #     E.compilation(
        #         E.command(self.commande_compil.data),
        #         E.point(str(self.points.data))),
        )
        cpt = 1
        for elem in self.tests:
            root.append(elem.toXml())
            cpt += 1
        return root


@server.route('/')
def home():
    form = FullForm()
    return render_template('home.html', form=form)


@server.route('/import', methods=['POST'])
def upload():
    form = FullForm()
    print(form.validate_on_submit())
    # setattr(form, 'a', FormField(Assert))
    # print(form.errors)
    # return render_template('home.html', form=form)
    test = etree.tostring(form.toXml(), xml_declaration=True, encoding='utf-8', pretty_print=True).decode('utf-8')
    return render_template('result.html', result=test)


@server.route('/add', methods=['POST'])
def change():
    form = FullForm()
    setattr(form, 'a', FormField(form.tests[0].test_type))
    return render_template('test.html', test=form.tests[0].form)


if __name__ == '__main__':
    server.run("0.0.0.0", port=5001, debug=True)
