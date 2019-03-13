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
import re

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
            print(self.test_assert_function.data)
            root = E.test(
                E.type(self.test_type.data),
                E.function(self.test_assert_function.data),
                E.result(self.test_assert_result.data),
                E.points(str(self.test_points.data))
            )

        if self.test_type.data == 'script':
            if not self.test_script.data:
                filename = ""
            else:
                filename = self.test_script.data.filename

            root = E.test(
                E.type(self.test_type.data),
                E.file(filename),
                E.points(str(self.test_points.data))
            )

        if self.test_type.data == 'motif':
            root = E.test(
                E.type(self.test_type.data),
                E.motif(self.test_motif.data),
                E.points(str(self.test_points.data))
            )

        return root

    def fromXml(self, element):
        self.test_type.data = element.find('type').text
        if element.find('points').text != 'None':
            self.test_points.data = float(element.find('points').text)

        if self.test_type.data == 'assert':
            self.test_assert_function.data = element.find('function').text
            self.test_assert_result.data = element.find('result').text

        if self.test_type.data == 'script':
            pass

        if self.test_type.data == 'motif':
            self.test_motif.data = element.find('motif').text

        return self


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
    name = TextField('Nom', [validators.DataRequired()])
    subject = FileField('Sujet PDF (optionnel)')
    codes = FileField('Exercices élèves')
    langage = SelectField('Langage', [validators.DataRequired()], choices=[('java', 'Java'), ('c', 'C')])
    commande_compil = TextField('Commande de compilation', [validators.DataRequired()])
    points = DecimalField('Points', [validators.DataRequired()])
    tests = FieldList(FormField(TestForm))
    submit = SubmitField('Submit')

    def toXml(self):
        root = E.tp(
            E.name(self.name.data),
            E.codes(),
            E.subject(),
            E.langage(self.langage.data),
            E.compilation(
                E.command(self.commande_compil.data),
                E.point(str(self.points.data))),
        )
        if self.subject.data != '':
            root.find('subject').text = self.subject.data.filename

        if self.codes.data != '':
            root.find('codes').text = self.codes.data.filename

        cpt = 1
        for elem in self.tests:
            root.append(elem.toXml())
            cpt += 1
        return root

    def fromXml(self, path):
        tree = etree.parse(path)
        root = tree.getroot()

        self.name.data = root.find('name').text
        self.langage.data = root.find('langage').text
        # self.subject.data = root.find('subject').text
        # self.codes.data.filename = root.find('codes')
        self.commande_compil.data = root.find('compilation').find('command').text

        if root.find('compilation').find('point').text != 'None':
            self.points.data = float(root.find('compilation').find('point').text)

        for idx, elem in enumerate(root.findall('test')):
            print(idx)
            t = TestForm().fromXml(elem)
            self.tests.append_entry(FieldList(TestForm()))
            self.tests[idx].test_type.data = t.test_type.data
            self.tests[idx].test_assert_function.data = t.test_assert_function.data
            self.tests[idx].test_assert_result.data = t.test_assert_result.data
            self.tests[idx].test_motif.data = t.test_motif.data
            self.tests[idx].test_points.data = t.test_points.data


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
    liste = os.listdir('saved_test')
    if 't' in request.args:
        full_path = os.path.join('saved_test', request.args.get('t'), request.args.get('t') + '.xml')
        form.fromXml(full_path)
    else:
        form.tests.append_entry()
    return render_template('test.html', form=form, liste=liste)


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
                    elem.test_script.data.save(os.path.join('saved_test', request.form.get('name'), filename))
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
    form = FullForm()

    if not form.name.data:
        print('error')
        return 'Nom requis'

    print(form.tests[0].test_assert_function)
    root = form.toXml()

    result = etree.tostring(root,
                            xml_declaration=True,
                            encoding='utf8',
                            pretty_print=True).decode('utf-8')
    print(result)

    path = os.path.normpath(form.name.data)
    sanitize_path = re.search('([A-Za-z0-9-_]+)', path)

    if sanitize_path:
        path = sanitize_path.group(1)
        if not os.path.isdir(os.path.join('saved_test', path)):
            os.mkdir(os.path.join('saved_test', path))

        with open(os.path.join('saved_test', path, path + '.xml'), 'w+') as f:
            f.write(result)

        if 'subject' in request.files:
            subject = request.files['subject']
            filename = secure_filename(subject.filename)
            subject.save(os.path.join('saved_test', path, filename))

        if 'codes' in request.files:
            codes = request.files['codes']
            filename = secure_filename(codes.filename)
            codes.save(os.path.join('saved_test', path, filename))

        for elem in form.tests:
            if elem.test_type.data == 'script':
                if elem.test_script.data != "":
                    filename = secure_filename(elem.test_script.data.filename)
                    elem.test_script.data.save(os.path.join('saved_test', path, filename))

    return "Enregistré"


@server.route('/list', methods=['GET'])
def liste():
    tests = os.listdir('saved_test')

    return render_template('liste.html', tests=tests)


if __name__ == '__main__':
    if not os.path.isdir('saved_test'):
        os.mkdir('saved_test')
        print('Folder for the saves is created')
    server.run("0.0.0.0", debug=True)
