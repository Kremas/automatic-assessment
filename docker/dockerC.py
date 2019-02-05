#! /usr/bin/python
# coding: utf-8

import docker
import sys
sys.path.insert(0, '../correction-c')

from xmlCClass import C
from os import getcwd


client = docker.from_env()

# List of the students
STUDENT = ['antoine', 'florian']
classname = 'calc'
for elem in STUDENT:
    testfile = C("../xml/test.xml", classname, "myapp")
    testfile.convert()
    testfile.toFile("includes")


makefile = ('HEADERS = myapp/' + classname + '.h\n'
            'OBJECTS = myapp/' + classname + '.o\n'
            'TARGET = ' + classname + '_test\n'
            'CFLAGS = -Wall\n'
            'LIBS = -lcunit\n'
            'CC = gcc\n'
            '\n'
            'all: $(OBJECTS) $(TARGET)\n'
            '\n'
            '$(OBJECTS): myapp/' + classname + '.c $(HEADERS)\n'
            '\t$(CC) $(CFLAGS) -c myapp/' + classname + '.c\n'
            '\n'
            '' + classname + '_test: ' + classname + '_test.c $(OBJECTS) $(HEADERS)\n'
            '\t$(CC) $(CFLAGS) -o $(TARGET) ' + classname + '_test.c $(OBJECTS) $(LIBS)\n'
            '\n'
            'clean:\n'
            '\t-rm -f $(OBJECTS)\n'
            '\t-rm -f $(TARGET)\n'
            )

with open('includes/Makefile', 'w') as f:
    f.write(makefile)


dockerfile = 'FROM alpine:latest \n\
RUN apk update && apk add gcc cunit-dev make libc-dev \n\
VOLUME /usr/src/myapp \n\
COPY includes/calc_test.c /usr/src/calc_test.c \n\
COPY includes/Makefile /usr/src/Makefile \n\
WORKDIR /usr/src/ \n\
ENTRYPOINT make && ./calc_test\n'

with open('dockerfile', 'w') as f:
    f.write(dockerfile)

# build the image
(img, l) = client.images.build(path='.',
                               tag='correction-c',
                               quiet=False
                               )

# run a container for each student
for elem in STUDENT:
    vol = {getcwd() + '/' + elem: {'bind': '/usr/src/myapp', 'mode': 'rw'}}
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

