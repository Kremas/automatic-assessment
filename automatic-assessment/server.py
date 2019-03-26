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
import zipfile
import docker
from pprint import pprint
import json
from shutil import rmtree

from helper.c.xmlCClass import C
from helper.c.dockerC import dockerC
from helper.cisco import *
from helper.java.xmlJavaClass import Java
from helper.java.dockerJava import dockerJava
from helper.java.searchRegex import Motif
from helper.python import xmlPythonClass

server = Flask(__name__)
server.config['SECRET_KEY'] = 'secretkey'
client = docker.from_env()


class TestForm(FlaskForm):
    '''
    Formulaire représentant un test

    :ivar TestForm.test_points:
        Points gagnés en réussissant ce test.
    :type TestForm.test_points: DecimalField

    :ivar TestForm.test_type:
        Type du test: assert(test unitaire), script, motif.
    :type TestForm.test_type: SelectField

    :ivar TestForm.test_assert_function:
        Fonction à tester en test unitaire. Forme: add(1, 2).
    :type TestForm.test_assert_functions: TextField

    :ivar TestForm.test_assert_result:
        Résultat attendu de la fonction.
    :type TestForm.test_assert_result: TextField

    :ivar TestForm.test_motif:
        Regex à chercher dans un code.
    :type TestForm.test_motif: TextField

    :ivar TestForm.test_script:
        Fichier de script à executer sur le code.
    :type TestForm.test_script: TextField

    :ivar TestForm.test_script_saved:
        Sauvegarde du nom du fichier de script
    :type TestForm.test_script_saved: TextField
    '''
    test_points = DecimalField("Points", [validators.DataRequired()])
    test_type = SelectField('Type', [validators.DataRequired()], choices=[('assert', 'Assert'), ('script', 'Script'), ('motif', 'Motif')], default='assert')
    test_assert_function = TextField("Fonction")
    test_assert_result = TextField("Résultat")
    test_motif = TextField("Motif")
    test_script = FileField("Script")
    # stockage du filename du script pour le reload
    test_script_saved = TextField()

    def toXml(self):
        '''
        Conversion du formulaire de test en fichier XML.
        '''
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
                if self.test_script_saved != '':
                    filename = self.test_script_saved.data

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
        '''
        Conversion d'un élément XML en formulaire

        :param element: Element XML à convertir
        :type element: etree.element
        '''
        self.test_type.data = element.find('type').text
        if element.find('points').text != 'None':
            self.test_points.data = float(element.find('points').text)

        if self.test_type.data == 'assert':
            self.test_assert_function.data = element.find('function').text
            self.test_assert_result.data = element.find('result').text

        if self.test_type.data == 'script':
            self.test_script_saved.data = element.find('file').text

        if self.test_type.data == 'motif':
            self.test_motif.data = element.find('motif').text

        return self


class TestCiscoForm(FlaskForm):
    '''
    :ivar TestCiscoForm.test_type:
        Type de catégorie à tester
    :type TestCiscoForm.test_type: SelectField

    :ivar TestCiscoForm.test_motif:
        Motif à rechercher dans la configuration
    :type TestCiscoForm.test_motif: TextAreaField

    :ivar TestCiscoForm.test_parent:

    :type TestCiscoForm.test_parent: TextField

    :ivar TestCiscoForm.test_points:
        Points à attribuer à ce test
    :type TestCiscoForm.test_points: DecimalField
    '''
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
    '''
    Formulaire complet incluant les différents tests

    :ivar FullForm.subject:
        Sujet PDF de l'examen
    :type FullForm.subject: FileField

    :ivar FullForm.subject_saved:
        Sauvegarde du nom du sujet
    :type FullForm.subject_saved: TextField

    :ivar FullForm.codes:
        Archive zip contenant les codes d'élèves à tester
    :type FullForm.codes: FileField

    :ivar FullForm.codes_saved:
        Sauvegarde du nom de l'archive zip contenant les codes d'élèves à tester
    :type FullForm.codes_saved: FileField

    :ivar FullForm.langage:
        Choix du langage de programmation utilisé dans les exercices
    :type FullForm.langage: SelectField

    :ivar FullForm.commande_compil:
        Ligne de commande pour compiler les exercices
    :type FullForm.commande_compil: TextField

    :ivar FullForm.points:
        Points attribués à une compilation réussie
    :type FullForm.points: DecimalField

    :ivar FullForm.tests:
        Liste contenant les différents :class:`TestForm`
    :type FullForm.tests: FieldList

    :ivar FullForm.submit:
        Soumission du formulaire
    :type FullForm.submit: SubmitField
    '''

    name = TextField('Nom', [validators.DataRequired()])
    subject = FileField('Sujet PDF (optionnel)')
    subject_saved = TextField()
    classname = TextField('Nom de la classe')
    codes = FileField('Exercices élèves')
    codes_saved = TextField()
    langage = SelectField('Langage', [validators.DataRequired()], choices=[('java', 'Java'), ('c', 'C')])
    commande_compil = TextField('Commande de compilation', [validators.DataRequired()])
    points = DecimalField('Points', [validators.DataRequired()])
    tests = FieldList(FormField(TestForm))
    submit = SubmitField('Submit')

    def toXml(self):
        '''
        Convertion du test global en fichier XML
        '''

        root = E.tp(
            E.name(self.name.data),
            E.classname(self.classname.data),
            E.codes(),
            E.subject(),
            E.langage(self.langage.data),
            E.compilation(
                E.command(self.commande_compil.data),
                E.point(str(self.points.data))),
        )
        # Si un nouveau fichier est spécifié, remplacer le sauvegardé
        if self.subject.data != '':
            root.find('subject').text = self.subject.data.filename
        elif (self.subject_saved.data != ''):
            root.find('subject').text = self.subject_saved.data

        if self.codes.data != '':
            root.find('codes').text = self.codes.data.filename
        elif (self.codes_saved.data != ''):
            root.find('codes').text = self.codes_saved.data

        cpt = 1
        for elem in self.tests:
            root.append(elem.toXml())
            cpt += 1
        return root

    def fromXml(self, path):
        '''
        Convertion d'un fichier XML en formulaire global
        '''
        tree = etree.parse(path)
        root = tree.getroot()
        self.codes_saved.data = root.find('codes').text
        self.subject_saved.data = root.find('subject').text
        self.classname.data = root.find('classname').text
        self.name.data = root.find('name').text
        self.langage.data = root.find('langage').text
        self.subject_saved.data = root.find('subject').text
        self.codes_saved.data = root.find('codes').text
        self.commande_compil.data = root.find('compilation').find('command').text

        if root.find('compilation').find('point').text != 'None':
            self.points.data = float(root.find('compilation').find('point').text)

        for idx, elem in enumerate(root.findall('test')):
            t = TestForm().fromXml(elem)
            self.tests.append_entry(FieldList(TestForm()))
            # Dégueulasse, mais necessaire, car append_entry ne passe pas les données et on ne peut pas remplacer l'objet
            self.tests[idx].test_type.data = t.test_type.data
            print(t.test_type.data)
            self.tests[idx].test_assert_function.data = t.test_assert_function.data
            self.tests[idx].test_assert_result.data = t.test_assert_result.data
            self.tests[idx].test_motif.data = t.test_motif.data
            self.tests[idx].test_points.data = t.test_points.data
            self.tests[idx].test_script_saved.data = t.test_script_saved.data


class FullCiscoForm(FlaskForm):
    '''
    Formulaire de test pour config cisco

    :ivar FullCiscoForm.tests:
        Liste de tests
    :type FullCiscoForm.tests: FieldList

    :ivar FullCiscoForm.submit:
        Soumission du formulaire
    :type FullCiscoForm.submit: SubmitField
    '''
    tests = FieldList(FormField(TestCiscoForm), min_entries=1)
    submit = SubmitField('Submit')

    def toXml(self):
        '''
        Convertion du formulaire global en objet xml
        '''
        root = E.tp()
        for elem in self.tests:
            root.append(elem.toXml())
        return root


@server.route('/')
def home():
    '''
    Sert la page principal du formulaire de test
        - methode: GET
        - chemin: /
    '''
    form = FullForm()
    liste = os.listdir('saved_test')
    if 't' in request.args:
        full_path = os.path.join('saved_test', request.args.get('t'), request.args.get('t') + '.xml')
        form.fromXml(full_path)
    else:
        form.tests.append_entry()
    debug(form)
    return render_template('test.html', form=form, liste=liste)


@server.route('/cisco')
def homeCisco():
    '''
    Sert la page de formulaire cisco
        - methode: GET
        - chemin: /cisco
    '''
    form = FullCiscoForm()
    return render_template('cisco.html', form=form)


@server.route('/import', methods=['POST'])
def upload():
    '''
    Endpoint permettant le lancement des tests de code
        - methode: POST
        - chemin: /import
    '''
    form = FullForm()

    if form.validate_on_submit():
        for elem in form.tests:
            if elem.test_type.data == 'script':
                if elem.test_script.data != "":
                    filename = secure_filename(elem.test_script.data.filename)
                    elem.test_script.data.save(os.path.join('saved_test', request.form.get('name'), filename))
                else:
                    return render_template('test.html', form=form, error="file required")

        root = form.toXml()

        if form.codes.data != '':
            f = secure_filename(form.codes.data.filename)
        elif form.codes_saved.data != '':
            f = secure_filename(form.codes_saved.data)
        else:
            return

        save()

        if zipfile.is_zipfile(os.path.join('saved_test', request.form.get('name'), f)):
            z = zipfile.ZipFile(os.path.join('saved_test', request.form.get('name'), f))
            all_list = z.namelist()
            codes_list = []
            for elem in all_list:
                if elem[-1] != '/':
                    codes_list.append(elem)
            # print(codes_list)
            z.extractall(path=os.path.join('saved_test', request.form.get('name')))
        else:
            codes_list = []
            codes_list.append(f)

        result = {}
        for elem in codes_list:
            result[elem] = {}

        if form.langage.data == 'java':
            s = Java(root, form.classname.data)
            s.convert()
            for elem in codes_list:
                s.toFile(path=os.path.join('saved_test', request.form.get('name'), os.path.dirname(elem)))

            d = dockerJava(codes_list, form.classname.data, form.name.data)

            if bool(d):
                for elem in d.ret:
                    print(json.loads(d.ret[elem])[1])
                    result[elem]['docker'] = json.loads(d.ret[elem])[1]
                    result[elem]['docker']['total'] = json.loads(d.ret[elem])[0]['total']

        elif form.langage.data == 'c':
            s = C(root, form.classname.data)
            s.convert()
            s.toFile(path=os.path.join('saved_test', request.form.get('name')))

            d = dockerC(codes_list, form.classname.data, form.name.data)

            if bool(d):
                for elem in d.ret:
                    print(d.ret[elem])
        else:
            return render_template('test.html', form=form, error={'Langage': 'Non reconnu'})

        for elem in codes_list:
            print(elem)
            m = Motif(root, os.path.join('saved_test', form.name.data, elem))
            print(m.search())
            result[elem]['motif'] = m.search()
            res = 0
            for key, val in result[elem]['motif'].items():
                res += float(val)

            result[elem]['motif']['total'] = res

            result[elem]['total'] = res
            if 'docker' in result[elem]:
                result[elem]['total'] += float(result[elem]['docker']['total'])
            print(result[elem]['total'])

        return render_template('result.html', result=result)
    else:
        return render_template('test.html', form=form, error=form.errors)


@server.route('/importCisco', methods=['POST'])
def uploadCisco():
    '''
    Endpoint permettant le lancement des tests de configuration cisco:
        - methode: POST
        - chemin: /importcisco
    '''
    form = FullCiscoForm()
    # print(form.validate_on_submit())
    # print(form.errors)
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
    '''
    Endpoint permettant l'enregistrement du formulaire et des fichiers uploadés
        - methode: POST
        - chemin: /save
    '''
    form = FullForm()
    if not form.name.data:
        print('error')
        return 'Nom requis'

    root = form.toXml()

    result = etree.tostring(root,
                            xml_declaration=True,
                            encoding='utf8',
                            pretty_print=True).decode('utf-8')
    # print(result)

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
    '''
    Endpoint permettant de lister tous les formulaires enregistrés
        - methode: GET
        - chemin: /list
    '''
    tests = os.listdir('saved_test')

    return render_template('liste.html', tests=tests)


@server.route('/delete', methods=['GET'])
def deleteTest():
    tests = os.listdir('saved_test')
    print(tests)
    if 't' in request.args:
        if request.args['t'] in tests:
            rmtree(os.path.join('saved_test', request.args['t']))
            tests = os.listdir('saved_test')
    return render_template('liste.html', tests=tests)


def debug(form):
    for field in form:
        pprint("{%s: %s}" % (field.name, field.data))


if __name__ == '__main__':
    if not os.path.isdir('saved_test'):
        os.mkdir('saved_test')
        print('Folder for the saves is created')
    server.run("0.0.0.0", debug=True)
