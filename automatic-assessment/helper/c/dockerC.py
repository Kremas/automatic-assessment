import docker
from os import getcwd, path


class dockerC(object):
    def __init__(self, codes, classname, name):
        self.client = docker.from_env()
        self.makefile = ('HEADERS = myapp/' + classname + '.h\n'
                         'OBJECTS = ' + classname + '.o\n'
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
        self.dockerfile = ('FROM alpine:latest \n'
                           'RUN apk update && apk add gcc cunit-dev make libc-dev \n'
                           'VOLUME /usr/src/myapp \n'
                           'COPY saved_test/' + name + '/' + classname + '_test.c /usr/src/' + classname + '_test.c \n'
                           'COPY saved_test/' + name + '/' + 'makefile /usr/src/Makefile \n'
                           'WORKDIR /usr/src/ \n'
                           'ENTRYPOINT make && ./calc_test\n'
                           )
        with open(path.join('saved_test', name, 'dockerfile'), 'w') as file:
            file.write(self.dockerfile)

        with open(path.join('saved_test', name, 'makefile'), 'w') as file:
            file.write(self.makefile)

        (img, l) = self.client.images.build(path='.',
                                            dockerfile=path.join('saved_test', name, 'dockerfile'),
                                            tag='correction-c',
                                            quiet=False,
                                            rm=True
                                            )
        for elem in l:
            if 'stream' in elem:
                print(elem['stream'].strip())
        self.ret = {}
        for elem in codes:
            if elem[-1:] == 'c':
                vol = {path.join(getcwd(), 'saved_test', name, path.dirname(elem)): {'bind': '/usr/src/myapp', 'mode': 'ro'}}
                container = ''
                try:
                    container = self.client.containers.run(img,
                                                           auto_remove=True,
                                                           stdout=True,
                                                           stderr=True,
                                                           volumes=vol)
                    # print(container.decode('utf-8'))
                    self.ret[elem] = container.decode('utf-8')
                except Exception as e:
                    print(e)
