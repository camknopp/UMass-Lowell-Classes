CC = clang++ -std=c++17

all: tests

tests: tests.cpp tombstones.h
	$(CC) -o tests.o  tests.cpp
	
clean:
	rm *.o tests