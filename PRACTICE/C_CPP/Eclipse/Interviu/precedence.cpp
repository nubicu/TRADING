/*
	A precedence rule is given as "P>E", which means that letter "P" is followed directly by the letter "E".
	Write a function, given an array of precedence rules, that finds the word represented by the given rules.
	Note: Each represented word contains a set of unique characters, i.e. the word does not contain duplicate letters.

	findWord({"P>E","E>R","R>U"}) // PERU
	findWord({"I>N","A>I","P>A","S>P"}) // SPAIN
	findWord({"R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G"}) // PORTUGAL

	*/
#include <vector>
#include <string>
#include <map>
#include <iostream>
using namespace std;

void recordLetter(map<char, int>& count, char letter1, char letter2)
{
    if (count.find(letter1) == count.end())
        count[letter1] = 1;
    else
        count[letter1]++;

    if (count.find(letter2) == count.end())
        count[letter2] = 1;
    else
        count[letter2]++;
}

/*
we create 2 separate arrays of letters and count
the number of characters resulting from the
original precedence array.
we look up the index of each letter from first letter
array and follow the index of the next letter.
*/
string findWord(const vector<string>& a) {
    size_t len = a.size();
    vector<char> firstLetter, secondLetter;
    size_t    currentIndex = 0;
    map<char, int> count;

    //count the number of repetitions for each letter
    while (currentIndex < len) {
        firstLetter.push_back(a[currentIndex].at(0));
        secondLetter.push_back(a[currentIndex].at(2));
        recordLetter(count, a[currentIndex].at(0), a[currentIndex].at(2));
        currentIndex++;
    }

    //The first letter should be in firstLetter array
    //and has count of 1.
    char first;
    for (map<char, int>::iterator it = count.begin(); it != count.end(); ++it)
    {
        char c = it->first;

        if (count[c] == 1)
        {
            for (vector<char>::iterator it1 = firstLetter.begin(); it1 != firstLetter.end(); ++it1)
            {
                if (*it1 == c)
                {
                    first = c;
                    break;
                }
            }
        }
    }

    string result;
    result += first;

    currentIndex = 0;
    for (size_t i = 0; i < firstLetter.size(); i++)
    {
        if (firstLetter[i] == first)
        {
            currentIndex = i;
            break;
        }
    }

    size_t times = 0;
    while (times < len) {
        result += secondLetter[currentIndex];

        for (size_t i = 0; i < firstLetter.size(); i++)
        {
            if (firstLetter[i] == secondLetter[currentIndex])
            {
                currentIndex = i;
                break;
            }
        }

        times++;
    }

    return result;
}

int main()
{
    cout << findWord({ "P>E", "E>R", "R>U"}) << endl; // PERU
	  cout << findWord({"I>N", "A>I", "P>A", "S>P"}) << endl; // SPAIN
    cout << findWord({ "U>N", "G>A", "R>Y", "H>U", "N>G", "A>R"}) << endl; // HUNGARY
    cout << findWord({ "I>F", "W>I", "S>W", "F>T" }) << endl;// SWIFT
    cout << findWord({ "R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G" }) << endl; // PORTUGAL
    cout << findWord({ "U>N", "G>A", "R>Y", "H>U", "N>G", "A>R" }) << endl;// HUNGARY
    cout << findWord({ "I>F", "W>I", "S>W", "F>T" }) << endl; // SWIFT
    cout << findWord({ "R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G" }) << endl;// PORTUGAL
    cout << findWord({ "W>I", "R>L", "T>Z", "Z>E", "S>W", "E>R", "L>A", "A>N", "N>D", "I>T" }) << endl; // SWITZERLAND

    return 0;
}
