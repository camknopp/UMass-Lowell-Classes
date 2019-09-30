// Copyright Cameron Knopp 2019
// Fall 2019 Foundations of Computer Science with Professor Jay McCarthy

#include <iostream>
#include <iterator>
#include <list>
#include <string>
#include <vector>

class myChar
{
public:
  explicit myChar(char c) { this->c = c; } // initialize char variable
  myChar() {}
  myChar(const myChar &charB) { c = charB.c; }
  void print() { std::cout << c; }
  char getVal() { return c; }
  myChar &operator=(const myChar &charB)
  {
    c = charB.c;
    return *this;
  }
  friend bool operator==(const myChar &a, const myChar &b)
  {
    return (a.c == b.c);
  }
  friend std::ostream &operator<<(std::ostream &os, const myChar &dt)
  {
    os << dt.c;
    return os;
  }

private:
  char c;
};

class myString
{
public:
  myString(char c, myString *nextString) : nextString(nextString)
  {
    this->c = myChar(c);
  }
  myString() {}
  virtual void print() { c.print(); }
  virtual myString *next() { return nextString; }
  virtual void test() { std::cout << "myString function" << std::endl; }
  virtual char charValue() { return c.getVal(); }
  virtual myChar charObject() { return c; }

private:
  myChar c;
  myString *nextString;
};

class oneString : public myString
{
public:
  oneString(char c, myString *nextString) : nextString(nextString)
  {
    this->c = myChar(c);
  }
  oneString() {}
  myString *next() { return nextString; }
  bool isEmpty() { return false; }
  void print() { c.print(); }
  void test() { std::cout << "oneString function" << std::endl; }
  char charValue() { return c.getVal(); }
  myChar charObject() { return c; }

private:
  myChar c;
  myString *nextString;
};

class emptyString : public myString
{
public:
  emptyString() { this->c = myChar('E'); } // needs to change E->actual epsilon
  bool isEmpty() { return true; }
  myString *next() { return NULL; }
  void print() { c.print(); }
  void test() { std::cout << "emptyString function" << std::endl; }
  char charValue() { return c.getVal(); }
  myChar charObject() { return c; }

private:
  myChar c;
};

template <class State>
class DFA
{
public:
  DFA<State>(std::string name, bool (*Q)(State), std::list<myChar> alphabet,
             State q0, State (*transFunc)(State, myChar), bool (*F)(State))
      : name(name), Q(Q), alphabet(alphabet), q0(q0), transFunc(transFunc),
        F(F) {}

  void printName() { std::cout << name << std::endl; }
  void printAlphabet()
  {
    for (auto a : alphabet)
      a.print();
  }

  bool accepts(myString &inputString)
  { // does DFA accept inputString?
    State qi = this->q0;
    myString *temp = &inputString;

    // step through DFA with the input string
    while (temp->charValue() != 'E')
    {
      qi = (*transFunc)(qi, temp->charObject());
      temp = temp->next();
    }

    return (*F)(qi); // checks whether arrived-at state is an accept state
  }

  void trace(myString &inputString)
  { // does DFA accept inputString?
    State qi = this->q0;
    myString *temp = &inputString;
    std::cout << qi;
    // step through DFA with the input string
    while (temp->charValue() != 'E')
    {
      qi = (*transFunc)(qi, temp->charObject());
      temp = temp->next();
      std::cout << qi;
    }
  }
  /*
  myString* acceptedString() {
    // need to check that accept states function is not empty by passing it
  possible

  }
*/
  bool acceptStates(myChar b) { return (*F)(b); } // used for testing
  State transitionFunction(State a, myChar b)
  {
    return (*transFunc)(a, b);
  } // used for testing

private:
  std::string name;
  bool (*Q)(State); // list of possible states for this dfa
  std::list<myChar> alphabet;
  State q0;                          // start state
  State (*transFunc)(State, myChar); // DFA transition function
  bool (*F)(State);                  // accept states
};

/*
myString lexi(std::list<myString> alphabet){

}
*/

// makes a DFA that only accepts a string of just one of the inputted Char
/*
DFA<myChar> oneCharDFA(myChar inputChar) {
  auto tFunc = [=](myChar a, myChar b) -> myChar {
    if (a.getVal() == 'A' && (b.getVal() == inputChar.getVal()))
      return myChar('B');
    else
      return myChar('C');
  };

  return DFA<myChar>("onlyAccepts" + std::string(1, inputChar.getVal()),
         [](myChar a) -> bool {
          return (a == myChar('A') || a == myChar('B'));
         },
         std::list<myChar>{inputChar},
         myChar('A'),
         &tFunc,
         [](myChar a) -> bool {
         return (a == myChar('B'));
         }
);
}
*/

void makeAndTestDFAs()
{

  DFA<myChar> evenLengthBinary(
      "EvenLengthBinary",    // name
      [](myChar a) -> bool { // state function
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('0'), myChar('1')}, // alphabet
      myChar('A'),                                 // start state
      [](myChar a, myChar b) -> myChar {           // transition function
        if ((a.getVal() == 'A') && ((b.getVal() == '0') || (b.getVal() == '1')))
          return myChar('B');
        else if ((a.getVal() == 'B') &&
                 ((b.getVal() == '0') || (b.getVal() == '1')))
          return myChar('A');
        else
          return a;
      },
      [](myChar a) -> bool { // accept states
        return (a.getVal() == 'A');
      });

  DFA<myChar> acceptsNothing(
      "AcceptsNothing", [](myChar a) -> bool { return false; },
      std::list<myChar>{}, myChar('A'),
      [](myChar a, myChar b) -> myChar { return a; },
      [](myChar a) -> bool { return false; });

  DFA<myChar> onlyAcceptsEmptyString(
      "OnlyAcceptsEmptyString",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('E')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() != 'E')
          return myChar('B');
        else if (a.getVal() == 'B')
          return myChar('B');
        else
          return a;
      },
      [](myChar a) -> bool { return (a == myChar('A')); });
  DFA<myChar> evenBinaryNumber(
      "EvenBinaryNumber",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if ((a.getVal() == 'A' || a.getVal() == 'B') && b.getVal() == '0')
          return myChar('B');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('B')); });

  DFA<myChar> oddBinaryNumber(
      "OddBinaryNumber",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if ((a.getVal() == 'A' || a.getVal() == 'B') && b.getVal() == '1')
          return myChar('B');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('B')); });

  DFA<myChar> containsCAM(
      "ContainsCAM",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B') ||
                (a.getVal() == 'C') || (a.getVal() == 'D'));
      },
      std::list<myChar>{myChar('C'), myChar('A'), myChar('M')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == 'C')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == 'A')
          return myChar('C');
        else if (a.getVal() == 'C' && b.getVal() == 'M')
          return myChar('D');
        else if (a.getVal() == 'D')
          return myChar('D'); // contains CAM, so we will remain in accept state
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('D')); });

  DFA<myChar> containsLineComment(
      "ContainsLineComment",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B') ||
                (a.getVal() == 'C'));
      },
      std::list<myChar>{myChar('/')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '/')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '/')
          return myChar('C');
        else if (a.getVal() == 'C')
          return myChar('C');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('C')); });

  DFA<myChar> threeConsecutiveZerosBinary(
      "ThreeConsecutiveZerosBinary",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B') ||
                (a.getVal() == 'C') || (a.getVal() == 'D'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '1')
          return myChar('A');
        else if (a.getVal() == 'A' && b.getVal() == '0')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '0')
          return myChar('C');
        else if (a.getVal() == 'C' && b.getVal() == '0')
          return myChar('D');
        else if (a.getVal() == 'D' && b.getVal() == '0')
          return myChar('B');
        else if (a.getVal() == 'D' && b.getVal() == '1')
          return myChar('D');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('D')); });

  DFA<myChar> threeConsecutiveOnesBinary(
      "ThreeConsecutiveOnesBinary",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B') ||
                (a.getVal() == 'C') || (a.getVal() == 'D'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '0')
          return myChar('A');
        else if (a.getVal() == 'A' && b.getVal() == '1')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '1')
          return myChar('C');
        else if (a.getVal() == 'C' && b.getVal() == '1')
          return myChar('D');
        else if (a.getVal() == 'D' && b.getVal() == '1')
          return myChar('B');
        else if (a.getVal() == 'D' && b.getVal() == '0')
          return myChar('D');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('D')); });

  DFA<myChar> oddNumberOfOnesBinary(
      "OddNumberOfOnesBinary",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '0')
          return myChar('A');
        else if (a.getVal() == 'A' && b.getVal() == '1')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '0')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '1')
          return myChar('A');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('B')); });
  DFA<myChar> evenNumberOfOnesBinary(
      "NumberOfOnesBinary",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '0')
          return myChar('A');
        else if (a.getVal() == 'A' && b.getVal() == '1')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '0')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '1')
          return myChar('A');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('A')); });

  DFA<myChar> evenNumberOfZerosAndSingleOne(
      "EvenNumberOfZerosAndSingleOne",
      [](myChar a) -> bool {
        return ((a.getVal() == 'A') || (a.getVal() == 'B') ||
                (a.getVal() == 'C'));
      },
      std::list<myChar>{myChar('1'), myChar('0')}, myChar('A'),
      [](myChar a, myChar b) -> myChar {
        if (a.getVal() == 'A' && b.getVal() == '0')
          return myChar('B');
        else if (a.getVal() == 'B' && b.getVal() == '0')
          return myChar('A');
        else if (a.getVal() == 'A' && b.getVal() == '1')
          return myChar('C');
        else
          return myChar('A');
      },
      [](myChar a) -> bool { return (a == myChar('C')); });

  oneString OZ = oneString('1', new oneString('0', new emptyString));
  oneString ZO = oneString('0', new oneString('1', new emptyString));
  oneString OZOO = oneString(
      '1', new oneString(
               '0', new oneString('1', new oneString('1', new emptyString))));
  oneString ZZZZ = oneString(
      '0', new oneString(
               '0', new oneString('0', new oneString('0', new emptyString))));
  oneString OOOOOO = oneString(
      '1',
      new oneString(
          '1',
          new oneString(
              '1', new oneString(
                       '1', new oneString(
                                '1', new oneString('1', new emptyString))))));
  emptyString epsi;
  oneString O = oneString('1', new emptyString);
  oneString Z = oneString('0', new emptyString);
  oneString OOO =
      oneString('1', new oneString('1', new oneString('1', new emptyString)));
  oneString ZOZ =
      oneString('0', new oneString('1', new oneString('0', new emptyString)));
  oneString ZZZZZ = oneString(
      '0',
      new oneString(
          '0',
          new oneString(
              '0', new oneString('0', new oneString('0', new emptyString)))));
  oneString ZOZOZ = oneString(

      '0',
      new oneString(
          '1',
          new oneString(
              '0', new oneString('1', new oneString('0', new emptyString)))));
  std::cout << std::boolalpha;
  std::cout << "-----------------------" << std::endl;
  std::cout << "Testing EvenLengthBinary DFA" << std::endl;
  std::cout << "1: Does EvenLengthBinary accept 10? " << evenLengthBinary.accepts(OZ)
            << std::endl;
  std::cout << "Trace for 10: ";
  evenLengthBinary.trace(OZ);
  std::cout << std::endl;
  std::cout << "2: Does EvenLengthBinary accept 01? " << evenLengthBinary.accepts(ZO)
            << std::endl;
  std::cout << "Trace for 01: ";
  evenLengthBinary.trace(ZO);
  std::cout << std::endl;
  std::cout << "3: Does EvenLengthBinary accept 1011? " << evenLengthBinary.accepts(OZOO)
            << std::endl;
  std::cout << "Trace for 1011: ";
  evenLengthBinary.trace(OZOO);
  std::cout << std::endl;
  std::cout << "4: Does EvenLengthBinary accept 0000? " << evenLengthBinary.accepts(ZZZZ)
            << std::endl;
  std::cout << "Trace for 0000: ";
  evenLengthBinary.trace(ZZZZ);
  std::cout << std::endl;
  std::cout << "5: Does EvenLengthBinary accept 111111? "
            << evenLengthBinary.accepts(OOOOOO) << std::endl;
  std::cout << "Trace for 111111: ";
  evenLengthBinary.trace(OOOOOO);
  std::cout << std::endl;
  std::cout << "6: Does EvenLengthBinary accept the empty string? "
            << evenLengthBinary.accepts(epsi) << std::endl;
  std::cout << "Trace for empty string: ";
  evenLengthBinary.trace(epsi);
  std::cout << std::endl;
  std::cout << "7: Does EvenLengthBinary accept 1? " << evenLengthBinary.accepts(O)
            << std::endl;
  std::cout << "Trace for 1: ";
  evenLengthBinary.trace(O);
  std::cout << std::endl;
  std::cout << "8: Does EvenLengthBinary accept 0? " << evenLengthBinary.accepts(Z)
            << std::endl;
  std::cout << "Trace for 0: ";
  evenLengthBinary.trace(Z);
  std::cout << std::endl;
  std::cout << "9: Does EvenLengthBinary accept 010? " << evenLengthBinary.accepts(ZOZ)
            << std::endl;
  std::cout << "Trace for 0: ";
  evenLengthBinary.trace(Z);
  std::cout << std::endl;
  std::cout << "10:Does EvenLengthBinary accept 00000? " << evenLengthBinary.accepts(ZZZZZ)
            << std::endl;
  std::cout << "Trace for 00000: ";
  evenLengthBinary.trace(ZZZZZ);
  std::cout << std::endl;
  std::cout << "11: Does EvenLengthBinary accept 111? " << evenLengthBinary.accepts(OOO)
            << std::endl;
  std::cout << "Trace for 111: ";
  evenLengthBinary.trace(OOO);
  std::cout << std::endl;
  std::cout << "12: Does EvenLengthBinary accept 01010? " << evenLengthBinary.accepts(ZOZOZ)
            << std::endl;
  std::cout << "Trace for 01010: ";
  evenLengthBinary.trace(ZOZOZ);
  std::cout << std::endl;
  std::cout << "-----------------------" << std::endl;

  std::cout << "-----------------------" << std::endl;
  std::cout << "Testing AcceptsNothing DFA" << std::endl;
  std::cout << "1: Does AcceptsNothing accept 10? " << acceptsNothing.accepts(OZ)
            << std::endl;
  std::cout << "Trace for 10: ";
  acceptsNothing.trace(OZ);
  std::cout << std::endl;
  std::cout << "2: Does AcceptsNothing accept 01? " << acceptsNothing.accepts(ZO)
            << std::endl;
  std::cout << "Trace for 01: ";
  acceptsNothing.trace(ZO);
  std::cout << std::endl;
  std::cout << "3: Does AcceptsNothing accept 1011? " << acceptsNothing.accepts(OZOO)
            << std::endl;
  std::cout << "Trace for 1011: ";
  acceptsNothing.trace(OZOO);
  std::cout << std::endl;
  std::cout << "4: Does AcceptsNothing accept 0000? " << acceptsNothing.accepts(ZZZZ)
            << std::endl;
  std::cout << "Trace for 0000: ";
  acceptsNothing.trace(ZZZZ);
  std::cout << std::endl;
  std::cout << "5: Does AcceptsNothing accept 111111? "
            << acceptsNothing.accepts(OOOOOO) << std::endl;
  std::cout << "Trace for 111111: ";
  acceptsNothing.trace(OOOOOO);
  std::cout << std::endl;
  std::cout << "6: Does AcceptsNothing accept the empty string? "
            << acceptsNothing.accepts(epsi) << std::endl;
  std::cout << "Trace for empty string: ";
  acceptsNothing.trace(epsi);
  std::cout << std::endl;
  std::cout << "7: Does AcceptsNothing accept 1? " << acceptsNothing.accepts(O)
            << std::endl;
  std::cout << "Trace for 1: ";
  acceptsNothing.trace(O);
  std::cout << std::endl;
  std::cout << "8: Does AcceptsNothing accept 0? " << acceptsNothing.accepts(Z)
            << std::endl;
  std::cout << "Trace for 0: ";
  acceptsNothing.trace(Z);
  std::cout << std::endl;
  std::cout << "9: Does AcceptsNothing accept 010? " << acceptsNothing.accepts(ZOZ)
            << std::endl;
  std::cout << "Trace for 0: ";
  acceptsNothing.trace(Z);
  std::cout << std::endl;
  std::cout << "10:Does AcceptsNothing accept 00000? " << acceptsNothing.accepts(ZZZZZ)
            << std::endl;
  std::cout << "Trace for 00000: ";
  acceptsNothing.trace(ZZZZZ);
  std::cout << std::endl;
  std::cout << "11: Does AcceptsNothing accept 111? " << acceptsNothing.accepts(OOO)
            << std::endl;
  std::cout << "Trace for 111: ";
  acceptsNothing.trace(OOO);
  std::cout << std::endl;
  std::cout << "12: Does AcceptsNothing accept 01010? " << acceptsNothing.accepts(ZOZOZ)
            << std::endl;
  std::cout << "Trace for 01010: ";
  acceptsNothing.trace(ZOZOZ);
  std::cout << std::endl;
  std::cout << "-----------------------" << std::endl;

  std::cout << "-----------------------" << std::endl;
  std::cout << "Testing OnlyAcceptsEmptyString DFA" << std::endl;
  std::cout << "1: Does OnlyAcceptsEmptyString accept 10? " << onlyAcceptsEmptyString.accepts(OZ)
            << std::endl;
  std::cout << "Trace for 10: ";
  onlyAcceptsEmptyString.trace(OZ);
  std::cout << std::endl;
  std::cout << "2: Does OnlyAcceptsEmptyString accept 01? " << onlyAcceptsEmptyString.accepts(ZO)
            << std::endl;
  std::cout << "Trace for 01: ";
  onlyAcceptsEmptyString.trace(ZO);
  std::cout << std::endl;
  std::cout << "3: Does OnlyAcceptsEmptyString accept 1011? " << onlyAcceptsEmptyString.accepts(OZOO)
            << std::endl;
  std::cout << "Trace for 1011: ";
  onlyAcceptsEmptyString.trace(OZOO);
  std::cout << std::endl;
  std::cout << "4: Does OnlyAcceptsEmptyString accept 0000? " << onlyAcceptsEmptyString.accepts(ZZZZ)
            << std::endl;
  std::cout << "Trace for 0000: ";
  onlyAcceptsEmptyString.trace(ZZZZ);
  std::cout << std::endl;
  std::cout << "5: Does OnlyAcceptsEmptyString accept 111111? "
            << onlyAcceptsEmptyString.accepts(OOOOOO) << std::endl;
  std::cout << "Trace for 111111: ";
  onlyAcceptsEmptyString.trace(OOOOOO);
  std::cout << std::endl;
  std::cout << "6: Does OnlyAcceptsEmptyString accept the empty string? "
            << onlyAcceptsEmptyString.accepts(epsi) << std::endl;
  std::cout << "Trace for empty string: ";
  onlyAcceptsEmptyString.trace(epsi);
  std::cout << std::endl;
  std::cout << "7: Does OnlyAcceptsEmptyString accept 1? " << onlyAcceptsEmptyString.accepts(O)
            << std::endl;
  std::cout << "Trace for 1: ";
  onlyAcceptsEmptyString.trace(O);
  std::cout << std::endl;
  std::cout << "8: Does OnlyAcceptsEmptyString accept 0? " << onlyAcceptsEmptyString.accepts(Z)
            << std::endl;
  std::cout << "Trace for 0: ";
  onlyAcceptsEmptyString.trace(Z);
  std::cout << std::endl;
  std::cout << "9: Does OnlyAcceptsEmptyString accept 010? " << onlyAcceptsEmptyString.accepts(ZOZ)
            << std::endl;
  std::cout << "Trace for 0: ";
  onlyAcceptsEmptyString.trace(Z);
  std::cout << std::endl;
  std::cout << "10:Does OnlyAcceptsEmptyString accept 00000? " << onlyAcceptsEmptyString.accepts(ZZZZZ)
            << std::endl;
  std::cout << "Trace for 00000: ";
  acceptsNothing.trace(ZZZZZ);
  std::cout << std::endl;
  std::cout << "11: Does OnlyAcceptsEmptyString accept 111? " << acceptsNothing.accepts(OOO)
            << std::endl;
  std::cout << "Trace for 111: ";
  onlyAcceptsEmptyString.trace(OOO);
  std::cout << std::endl;
  std::cout << "12: Does OnlyAcceptsEmptyString accept 01010? " << onlyAcceptsEmptyString.accepts(ZOZOZ)
            << std::endl;
  std::cout << "Trace for 01010: ";
  onlyAcceptsEmptyString.trace(ZOZOZ);
  std::cout << std::endl;
  std::cout << "-----------------------" << std::endl;

  std::cout << "-----------------------" << std::endl;
  std::cout << "Testing EvenBinaryNumber DFA" << std::endl;
  std::cout << "1: Does EvenBinaryNumber accept 10? " << evenBinaryNumber.accepts(OZ)
            << std::endl;
  std::cout << "Trace for 10: ";
  evenBinaryNumber.trace(OZ);
  std::cout << std::endl;
  std::cout << "2: Does EvenBinaryNumber accept 01? " << evenBinaryNumber.accepts(ZO)
            << std::endl;
  std::cout << "Trace for 01: ";
  evenBinaryNumber.trace(ZO);
  std::cout << std::endl;
  std::cout << "3: Does EvenBinaryNumber accept 1011? " << evenBinaryNumber.accepts(OZOO)
            << std::endl;
  std::cout << "Trace for 1011: ";
  evenBinaryNumber.trace(OZOO);
  std::cout << std::endl;
  std::cout << "4: Does EvenBinaryNumber accept 0000? " << evenBinaryNumber.accepts(ZZZZ)
            << std::endl;
  std::cout << "Trace for 0000: ";
  evenBinaryNumber.trace(ZZZZ);
  std::cout << std::endl;
  std::cout << "5: Does EvenBinaryNumber accept 111111? "
            << evenBinaryNumber.accepts(OOOOOO) << std::endl;
  std::cout << "Trace for 111111: ";
  evenBinaryNumber.trace(OOOOOO);
  std::cout << std::endl;
  std::cout << "6: Does EvenBinaryNumber accept the empty string? "
            << evenBinaryNumber.accepts(epsi) << std::endl;
  std::cout << "Trace for empty string: ";
  evenBinaryNumber.trace(epsi);
  std::cout << std::endl;
  std::cout << "7: Does EvenBinaryNumber accept 1? " << evenBinaryNumber.accepts(O)
            << std::endl;
  std::cout << "Trace for 1: ";
  evenBinaryNumber.trace(O);
  std::cout << std::endl;
  std::cout << "8: Does EvenBinaryNumber accept 0? " << evenBinaryNumber.accepts(Z)
            << std::endl;
  std::cout << "Trace for 0: ";
  evenBinaryNumber.trace(Z);
  std::cout << std::endl;
  std::cout << "9: Does EvenBinaryNumber accept 010? " << evenBinaryNumber.accepts(ZOZ)
            << std::endl;
  std::cout << "Trace for 0: ";
  evenBinaryNumber.trace(Z);
  std::cout << std::endl;
  std::cout << "10:Does EvenBinaryNumber accept 00000? " << evenBinaryNumber.accepts(ZZZZZ)
            << std::endl;
  std::cout << "Trace for 00000: ";
  evenBinaryNumber.trace(ZZZZZ);
  std::cout << std::endl;
  std::cout << "11: Does EvenBinaryNumber accept 111? " << evenBinaryNumber.accepts(OOO)
            << std::endl;
  std::cout << "Trace for 111: ";
  evenBinaryNumber.trace(OOO);
  std::cout << std::endl;
  std::cout << "12: Does EvenBinaryNumber accept 01010? " << evenBinaryNumber.accepts(ZOZOZ)
            << std::endl;
  std::cout << "Trace for 01010: ";
  evenBinaryNumber.trace(ZOZOZ);
  std::cout << std::endl;
  std::cout << "-----------------------" << std::endl;

  std::cout << "-----------------------" << std::endl;
  std::cout << "Testing OddBinaryNumber DFA" << std::endl;
  std::cout << "1: Does OddBinaryNumber accept 10? " << oddBinaryNumber.accepts(OZ)
            << std::endl;
  std::cout << "Trace for 10: ";
  oddBinaryNumber.trace(OZ);
  std::cout << std::endl;
  std::cout << "2: Does OddBinaryNumber accept 01? " << oddBinaryNumber.accepts(ZO)
            << std::endl;
  std::cout << "Trace for 01: ";
  oddBinaryNumber.trace(ZO);
  std::cout << std::endl;
  std::cout << "3: Does OddBinaryNumber accept 1011? " << oddBinaryNumber.accepts(OZOO)
            << std::endl;
  std::cout << "Trace for 1011: ";
  oddBinaryNumber.trace(OZOO);
  std::cout << std::endl;
  std::cout << "4: Does OddBinaryNumber accept 0000? " << oddBinaryNumber.accepts(ZZZZ)
            << std::endl;
  std::cout << "Trace for 0000: ";
  oddBinaryNumber.trace(ZZZZ);
  std::cout << std::endl;
  std::cout << "5: Does OddBinaryNumber accept 111111? "
            << oddBinaryNumber.accepts(OOOOOO) << std::endl;
  std::cout << "Trace for 111111: ";
  oddBinaryNumber.trace(OOOOOO);
  std::cout << std::endl;
  std::cout << "6: Does OddBinaryNumber accept the empty string? "
            << oddBinaryNumber.accepts(epsi) << std::endl;
  std::cout << "Trace for empty string: ";
  oddBinaryNumber.trace(epsi);
  std::cout << std::endl;
  std::cout << "7: Does OddBinaryNumber accept 1? " << oddBinaryNumber.accepts(O)
            << std::endl;
  std::cout << "Trace for 1: ";
  oddBinaryNumber.trace(O);
  std::cout << std::endl;
  std::cout << "8: Does OddBinaryNumber accept 0? " << oddBinaryNumber.accepts(Z)
            << std::endl;
  std::cout << "Trace for 0: ";
  oddBinaryNumber.trace(Z);
  std::cout << std::endl;
  std::cout << "9: Does OddBinaryNumber accept 010? " << oddBinaryNumber.accepts(ZOZ)
            << std::endl;
  std::cout << "Trace for 0: ";
  oddBinaryNumber.trace(Z);
  std::cout << std::endl;
  std::cout << "10:Does OddBinaryNumber accept 00000? " << oddBinaryNumber.accepts(ZZZZZ)
            << std::endl;
  std::cout << "Trace for 00000: ";
  oddBinaryNumber.trace(ZZZZZ);
  std::cout << std::endl;
  std::cout << "11: Does EvenBinaryNumber accept 111? " << oddBinaryNumber.accepts(OOO)
            << std::endl;
  std::cout << "Trace for 111: ";
  oddBinaryNumber.trace(OOO);
  std::cout << std::endl;
  std::cout << "12: Does BinaryNumber accept 01010? " << oddBinaryNumber.accepts(ZOZOZ)
            << std::endl;
  std::cout << "Trace for 01010: ";
  oddBinaryNumber.trace(ZOZOZ);
  std::cout << std::endl;
  std::cout << "-----------------------" << std::endl;
}

int main()
{
  int answer;

  std::cout << "Please enter the number of the machine you wish to simulate" << std::endl;
  std::cout << "1: DFA" << std::endl;
  std::cout << "10: Exit simulator" << std::endl;

  while (true)
  {
    std::cin >> answer;

    if (answer == 1)
      makeAndTestDFAs();
    else if (answer == 10)
      break;
    else
      std::cout << "Please enter a valid number between 1 and 10: " << std::endl;
  }
  return 0;
}
