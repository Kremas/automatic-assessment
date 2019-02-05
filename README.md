# Automatic assessment
## xmlJavaClass.py
Convertit un fichier xml en test unitaire (JUnit).
#### Generation du test
    python xmlJavaClass.py
#### Compilation du test
    javac -cp junit-4.13-beta-1.jar:hamcrest-all-1.3.jar:. MaClasseTest.java TestRunner.java
#### Usage
    java -cp hamcrest-all-1.3.jar:junit-4.13-beta-1.jar:. TestRunner


## Dockerjava
* Crée un dockerfile dans le dossier courant
    ``` dockerfile
    FROM openjdk:8u131-jdk-alpine
    VOLUME /src
    ADD includes /includes
    WORKDIR /src
    ENTRYPOINT javac -cp /includes/junit-4.13-beta-1.jar:/includes/hamcrest-all-1.3.jar:. MaClasseTest.java /includes/TestRunner.java -d . && 
            java -cp /includes/hamcrest-all-1.3.jar:/includes/junit-4.13-beta-1.jar:. TestRunner
    ```

* Lance un container par étudiant en montant le dossier `nom`.  
Le container compile la classe et le test, exécute le test et renvoie le résultat sous la forme
    ``` xml
    antoine
    <result>
    <testrun>4</testrun>
      <failure>
      </failure>
    <success>true</success>
    </resultat 
    florian
    <result>
    <testrun>4</testrun>
      <failure>
        <test>
          <function>divide(MaClasseTest)</function>
          <message>/ by zero</message>
        </test>
        <test>
          <function>sub(MaClasseTest)</function>
          <message>sub(5,2) expected:<3.0> but was:<4.0></message>
        </test>
      </failure>
    <success>false</success>
    </resultat
    ```
* Les containers sont detruits (mais l'image, non !). Donc penser à utiliser  
    `docker rmi image_id`

#### Structure
* student1/
  * Class.java
  * **ClassTest.java** (crée automatiquement)
* student2/
  * Class.java
  * **ClassTest.java** (crée automatiquement)
* includes/
  * hamcrest.jar
  * junit4.jar
  * TestRunner.java

## DockerC
* Crée un dockerfile dans le dossier courant
    ``` dockerfile
    FROM alpine:latest 
    RUN apk update && apk add gcc cunit-dev make libc-dev 
    VOLUME /usr/src/myapp 
    COPY includes/calc_test.c /usr/src/calc_test.c 
    COPY includes/Makefile /usr/src/Makefile 
    WORKDIR /usr/src/ 
    ENTRYPOINT make && ./calc_test
    ```
* idem

#### Structure
* student1/
  * file.c
  * file.h
* student2/
  * file.c
  * file.h
* includes/
  * **Makefile** (crée automatiquement)
  * **calc_test.c** (crée automatiquement)