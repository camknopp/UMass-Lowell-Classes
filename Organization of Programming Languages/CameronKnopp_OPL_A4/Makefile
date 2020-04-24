CC = clang++ -std=c++17
OBJECTS = tests.o 

all: tests

tests: tests.o
	$(CC) $(OBJECTS) -o $@

$(OBJECTS): tests.cpp
	$(CC) tests.cpp -c

clean:
	rm *.o tests