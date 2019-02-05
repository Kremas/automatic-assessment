#! /usr/bin/python
# coding: utf-8

import docker
import sys
sys.path.insert(0, '../correction-java')
from xmlJavaClass import Java
from pprint import pprint
from os import getcwd

client = docker.from_env()

# List of the students
STUDENT = ['antoine', 'florian']

for elem in STUDENT:
    testfile = Java('../correction-java/maclasse.xml', "MaClasse")
    testfile.convert()
    testfile.toFile(elem)


dockerfile = 'FROM openjdk:8u131-jdk-alpine\n\
VOLUME /src\n\
ADD includes /includes\n\
WORKDIR /src\n\
ENTRYPOINT javac -cp /includes/junit-4.13-beta-1.jar:/includes/hamcrest-all-1.3.jar:. ' + testfile.classname + 'Test.java /includes/TestRunner.java -d . && java -cp /includes/hamcrest-all-1.3.jar:/includes/junit-4.13-beta-1.jar:. TestRunner\n'

with open('dockerfile', 'w') as f:
    f.write(dockerfile)

# build the image
(img, l) = client.images.build(path='.',
                               tag='correction-java',
                               quiet=False
                               )

# run a container for each student
for elem in STUDENT:
    vol = {getcwd() + '/' + elem: {'bind': '/src', 'mode': 'rw'}}
    container = ''

    try:
        container = client.containers.run(img,
                                          auto_remove=True,
                                          stdout=True,
                                          stderr=True,
                                          volumes=vol)
        print(elem)
        print(container.decode('utf-8'))

    except Exception as e:
        print(e)

