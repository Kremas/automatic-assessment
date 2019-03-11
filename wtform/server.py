#! /usr/bin/python3
# coding: utf8

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, SubmitField, FieldList, FormField, DecimalField, validators, FileField, TextAreaField
from lxml.builder import E
from lxml import etree
from werkzeug import secure_filename
from pprint import pprint
import os

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


class TestCiscoForm(FlaskForm):
    test_type = SelectField('Type',
                            [validators.DataRequired()],
                            choices=[('misc', 'Misc'),
                                     ('interface', 'Interface configuration'),
                                     ('router ospf', 'OSPF configuration'),
                                     ('router isis', 'IS-IS configuration'),
                                     ('router eigrp', 'EIGRP configuration'),
                                     ('router rip', 'RIP configuration'),
                                     ('router bgp', 'BGP configuration'),
                                     ('line', 'Line configuration')
                                    ],
                            default='interface'
                           )
    test_motif = TextAreaField("Motif")
    test_parent = TextField("Parent")
    test_points = DecimalField("Points", [validators.DataRequired()])

    def toXml(self):
        root = E.test()
        if self.test_type.data == 'misc':
            root = E.test(
                E.type(self.test_type.data),
                E.textarea(self.test_motif.data),
                E.points(str(self.test_points.data))
            )
        else:
            root = E.test(
                E.type(self.test_type.data),
                E.parent(self.test_parent.data),
                E.textarea(self.test_motif.data),
                E.points(str(self.test_points.data))
            )
        return root


class FullForm(FlaskForm):
    subject = FileField('Sujet PDF')
    codes = FileField('Exercices élèves')
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


class FullCiscoForm(FlaskForm):
    tests = FieldList(FormField(TestCiscoForm), min_entries=1)
    submit = SubmitField('Submit')

    def toXml(self):
        root = E.tp()
        for elem in self.tests:
            root.append(elem.toXml())
        return root


@server.route('/')
def home():
    form = FullForm()
    return render_template('test.html', form=form)


@server.route('/cisco')
def homeCisco():
    form = FullCiscoForm()
    return render_template('cisco.html', form=form)


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


@server.route('/importCisco', methods=['POST'])
def uploadCisco():
    form = FullCiscoForm()
    print(form.validate_on_submit())
    print(form.errors)
    result = ""
    if form.validate_on_submit():
        root = form.toXml()
        result = etree.tostring(root,
                                xml_declaration=True,
                                encoding='utf8',
                                pretty_print=True).decode('utf-8')
        return render_template('result.html', result=result)
    else:
        return render_template('cisco.html', form=form, error=form.errors)


@server.route('/save', methods=['POST'])
def save():
    pprint(request.form)


    # to XML
    i = 0
    root = E.tp(
        E.langage(request.form['langage']),
        E.compilation(
            E.command(request.form['commande_compil']),
            E.points(request.form['points'])
        )
    )
    test_xml = E.test()
    i = 0
    for elem in request.form:
        if str(i) in elem:
            if(request.form[("tests-" + str(i) + "-test_type")] == "assert"):
                test_xml = E.test(
                    E.type('assert'),
                    E.function(request.form[("tests-" + str(i) + "-test_assert_function")]),
                    E.result(request.form[("tests-" + str(i) + "-test_assert_result")]),
                    E.points(request.form[("tests-" + str(i) + "-test_points")]),
                )
            if(request.form[("tests-" + str(i) + "-test_type")] == "motif"):
                test_xml = E.test(
                    E.type('motif'),
                    E.motif(request.form[("tests-" + str(i) + "-test_motif")]),
                    E.points(request.form[("tests-" + str(i) + "-test_points")]),
                )
            if("test_points" in elem):
                i += 1
                root.append(test_xml)
    result = etree.tostring(root,
                            xml_declaration=True,
                            encoding='utf8',
                            pretty_print=True).decode('utf-8')
    print(result)
    if not os.path.isdir('saved_test/' + request.form['name']):
        os.mkdir('saved_test/' + request.form['name'])

    with open('saved_test/' + request.form['name'] + '/' + request.form['name'] + '.xml', 'w+') as f:
        f.write(result)

    return "Bien reçu"


if __name__ == '__main__':
    if not os.path.isdir('saved_test'):
        os.mkdir('saved_test')
        print('Folder for the saves is created')
    server.run("0.0.0.0", debug=True)
