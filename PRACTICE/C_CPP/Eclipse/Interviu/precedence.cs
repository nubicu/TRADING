/*
	A precedence rule is given as "P>E", which means that letter "P" is followed directly by the letter "E".
	Write a function, given an array of precedence rules, that finds the word represented by the given rules.
	Note: Each represented word contains a set of unique characters, i.e. the word does not contain duplicate letters.

	findWord(["P>E","E>R","R>U"]) // PERU
	findWord(["I>N","A>I","P>A","S>P"]) // SPAIN
	findWord(["R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G"]) // PORTUGAL

	*/

/*
Solutie C#:
*/
using System;
using System.Collections.Generic;
using System.Linq;

public class Program
{
	public static void Main()
	{
		Console.WriteLine(findWord(new string[]{"P>E","E>R","R>U"})); // PERU
		Console.WriteLine(findWord(new string[]{"I>N","A>I","P>A","S>P"})); // SPAIN
		Console.WriteLine(findWord(new string[]{"R>T", "A>L", "P>O", "O>R", "G>A", "T>U", "U>G"})); // PORTUGAL
	}

	static string findWord(string[] precedences){
		var prec = precedences.ToList();
		string final = "";

		var p = prec.First();
		final = p[0].ToString() + p[2].ToString();

		prec = prec.Skip(1).ToList();

		while (prec.Any())
		{
			var nextP = prec.FirstOrDefault(c=> c[0] == final[final.Length-1]);

			if (nextP != null)
			{
				final += nextP[2];
			}
			else
			{
				nextP = prec.FirstOrDefault(c=> c[2] == final[0]);

				if (nextP != null)
				{
					final = nextP[0] + final;
				}
			}

			prec.Remove(nextP);
		}

		return final;
	}
}
/* */
