HEADERS = myapp/calc.h
OBJECTS = calc.o
TARGET = calc_test
CFLAGS = -Wall
LIBS = -lcunit
CC = gcc

all: $(OBJECTS) $(TARGET)

$(OBJECTS): myapp/calc.c $(HEADERS)
	$(CC) $(CFLAGS) -c myapp/calc.c

calc_test: calc_test.c $(OBJECTS) $(HEADERS)
	$(CC) $(CFLAGS) -o $(TARGET) calc_test.c $(OBJECTS) $(LIBS)

clean:
	-rm -f $(OBJECTS)
	-rm -f $(TARGET)
