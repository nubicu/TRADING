#include <iostream>
using namespace std;

int main()
{
    int N, M, i = 0, j = 0, k = 0;;

    cin>>N;
    int v[N];
    for (i=0;i<N;i++){
        cin>>v[i];
    }

    cin>>M;
    int w[M], rez[M+N];
    for (i=0;i<M;i++){
        cin>>w[i];
    }

    i = 0;
    j = 0;
    while(i < N && j < M)
    {
        if(v[i] < w[j])
        {
            rez[k] = v[i];
            k++;
            i++;
        }
        else
        {
            rez[k] = w[j];
            k++;
            j++;
        }
    }

    if(i <= N)
    {
        for(int p = i; p < N; p++)
        {
            rez[k] = v[p];
            k++;
        }
    }
    if(j <= M)
    {
        for(int p = j; p < M; p++)
        {
            rez[k] = w[p];
            k++;
        }
    }

     for(int p = 0; p < k; p++)
        cout << rez[p] << " ";

    return 0;
}
