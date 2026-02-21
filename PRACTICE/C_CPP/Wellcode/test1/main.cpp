#include <iostream>
#include <climits>
using namespace std;

int main() {
  int n, max=INT_MIN, min=INT_MAX;
  cin >> n;
  int a[n];
    for (int i=0;i<n;i++) {
        cin >> a[i];
        if(max<a[i])
            max = a[i];
        if (min > a[i])
            min = a[i];
    }

    cout << min << " " << max;
  return 0;
}
