import docker
from os import getcwd, path


class dockerJava(object):
    def __init__(self, codes, c, name):
        with open('helper/java/includes/TestRunner.java', 'r') as file:
            with open(path.join(getcwd(), 'saved_test', name, 'TestRunner.java'), 'w') as file2:
                file2.write(file.read().replace('TACTACTAChaha', c + 'Test'))

        self.client = docker.from_env()
        self.dockerfile = 'FROM openjdk:8u131-jdk-alpine\n\
    VOLUME /src\n\
    ADD helper/java/includes /includes\n\
    ADD saved_test/' + name + '/TestRunner.java /includes/TestRunner.java\n\
    WORKDIR /src\n\
    ENTRYPOINT javac -cp /includes/junit-4.13-beta-1.jar:/includes/hamcrest-all-1.3.jar:. ' + c + 'Test.java /includes/TestRunner.java -d . && java -cp /includes/hamcrest-all-1.3.jar:/includes/junit-4.13-beta-1.jar:. TestRunner\n'
        with open(path.join('saved_test', name, 'dockerfile'), 'w') as file:
            file.write(self.dockerfile)

        (img, l) = self.client.images.build(path='.',
                                            dockerfile=path.join('saved_test', name, 'dockerfile'),
                                            tag='correction-java',
                                            quiet=False
                                            )
        self.ret = {}
        for elem in codes:
            vol = {path.join(getcwd(), 'saved_test', name, path.dirname(elem)): {'bind': '/src', 'mode': 'rw'}}
            container = ''
            try:
                container = self.client.containers.run(img,
                                                       auto_remove=True,
                                                       stdout=True,
                                                       stderr=True,
                                                       volumes=vol)

                self.ret[elem] = container.decode('utf-8')
            except Exception as e:
                print(e)
