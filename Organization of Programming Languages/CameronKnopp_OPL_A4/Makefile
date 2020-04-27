CC = clang++ -std=c++17

tests: tests.o
	$(CC) tests.o -o $@

tests.o: tests.cpp 
	$(CC) -c tests.cpp 

clean:
	rm *.o tests