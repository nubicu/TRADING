// Service Lane
// link : https://www.hackerrank.com/challenges/service-lane/problem
/* 
Calvin is driving his favorite vehicle on the 101 freeway. He notices that the check engine light of his vehicle is on, and he wants to service it immediately to avoid any risks. Luckily, a service lane runs parallel to the highway. The service lane varies in width along its length.
You will be given an array of widths at points along the road (indexes), then a list of the indexes of entry and exit points. Considering each entry and exit point pair, calculate the maximum size vehicle that can travel that segment of the service lane safely.
Complete the code stub below to return an array of integers representing the values calculated.
Input Format : The first line of input contains two integers, n(number of width measurements you will receive)and t(number of test cases). The next line has n space-separated integers which represent the array width[w0,w1,...,wn-1].
The next t lines contain two integers : i(start index) and j(end index of the segment being considered).
Constraints : 2<=n<=100000; 1<=t<=1000; 0<=i<j<n; 2<=j-i+1<=min(n,1000); 1<=width[k]<=3, where 0<=k<n
Output Format : For each test case, print the number that represents the largest vehicle type that can pass through the entire segment of the service lane between indexes i and j inclusive.
*/

#include <bits/stdc++.h>
#include <vector>
using namespace std;

vector<int> serviceLane(int n, vector<vector<int>> cases, vector<int> width) {
    vector<int> returnVector;
    int entry,exit,current_vehicle,largest_vehicle=3;
    for(int cases_i = 0;cases_i < n;cases_i++){
       for(int cases_j = 0;cases_j < 2;cases_j++){
           for(int check_index=cases_i;check_index<cases_j;check_index++)
           if (width[check_index] == 1) {current_vehicle=1;}
           else if(width[check_index] == 2) {current_vehicle=2;}
           else {current_vehicle=3;}
           
           if(current_vehicle<largest_vehicle) {largest_vehicle=current_vehicle;}
        }
        returnVector.push_back(largest_vehicle);        
    }
    
    return returnVector;
}

int main() {
    int n; // number of width measurements you will receive
    int t; // number of test cases
    cin >> n >> t;
    vector<int> width(n);
    for(int width_i = 0; width_i < n; width_i++){
       cin >> width[width_i]; // lane width
    }
    vector<vector<int>> cases(t,vector<int>(2));
    for(int cases_i = 0;cases_i < t;cases_i++){
       for(int cases_j = 0;cases_j < 2;cases_j++){
          cin >> cases[cases_i][cases_j];
       }
    }
    vector<int> result = serviceLane(n, cases, width);
    for (ssize_t i = 0; i < result.size(); i++) {
        cout << result[i] << (i != result.size() - 1 ? "\n" : "");
    }
    cout << endl;


    return 0;
}

/*
Sample Input :
8 5
2 3 1 2 3 2 3 3
0 3
4 6
6 7
3 5
0 7
Sample Output :
1
2
3
2
1
*/

/* Explanation :
Below is the representation of the lane:
   |HIGHWAY|Lane|    ->    Width
0: |       |--|            2
1: |       |---|           3
2: |       |-|             1
3: |       |--|            2
4: |       |---|           3
5: |       |--|            2
6: |       |---|           3
7: |       |---|           3
*/
