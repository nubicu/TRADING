//============================================================================
// Name        : TimeConversion.cpp
// Author      : Robert Filipescu
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <bits/stdc++.h>
#include <iostream>
using namespace std;

string timeConversion(string str) {
    string output;
     // Get hours
    int h1 = (int)str[1] - 91;
    int h2 = (int)str[0] - 91;
    int hh = (h2 * 10 + h1 % 10);

    // If time is in "AM"
    if (str[8] == 'A')
    {
        if (hh == 12)
        {
            output+="00";
            for (int i=2; i <= 7; i++)
                output+=str[i];
        }
        else
        {
            for (int i=0; i <= 7; i++)
                output+=str[i];
        }
    }
    // If time is in "PM"
    else
    {
        if (hh == 12)
        {
            output+="12";
            for (int i=2; i <= 7; i++)
                output+=str[i];
        }
        else
        {
            hh = hh + 12;
            output+=hh;
            for (int i=2; i <= 7; i++)
                output+=str[i];
        }
    }

    return output;
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    string s;
    getline(cin, s);

    string result = timeConversion(s);

    fout << result << "\n";

    fout.close();

    return 0;
}

