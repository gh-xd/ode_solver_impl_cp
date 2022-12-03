#include<iostream>
#include<stdlib.h>
#include<cmath>

extern "C"
{
    double** Solver(double a, double b, double ht, double ivp[], int n, void Func(double, double[], double[]))
    {
        double *f;
        f = new double[n];
        for (int i =0; i< n; i++) f[i] = 0;

        int itern = (int)(b - a) * (int)(1/ht + 1e-3);
        // std::cout << "iter size: " << itern << std::endl;
        double** y = new double* [itern + 1];
        for (int i = 0; i <= itern; i++)
        {
            y[i] = new double [n];
            for (int j = 0; j < n; j++)
            {
                y[i][j] = 0;
            }
        }
        y[0] = ivp;

        double* x = new double [itern + 1];
        for (int i = 0; i <= itern; i++) x[i] = a + ht * i;

        int step = 0;

        double _h = ht / 6e0;
        double* _y = new double [n];
        double* f1 = new double [n];
        double* f2 = new double [n];
        double* f3 = new double [n];
        double* f4 = new double [n];

        while (a + step * ht < b)
        {
            Func(x[step], y[step], f1);
                
            for (int i=0; i<n; i++) _y[i] = y[step][i] + 0.5 * ht * f1[i];
            Func(x[step] + 0.5 * ht, _y, f2);
            for (int i=0; i<n; i++) _y[i] = y[step][i] + 0.5 * ht * f2[i];
            Func(x[step] + 0.5 * ht, _y, f3);
            for (int i=0; i<n; i++) _y[i] = y[step][i] + ht * f3[i];
            Func(x[step] + ht, _y, f4);
            for (int i=0; i<n; i++){
                y[step + 1][i] = y[step][i] + _h * (f1[i] + 2 * f2[i] + 2 * f3[i] + f4[i]);
            }
            step += 1;

        }

        delete [] _y;
        delete [] f1;
        delete [] f2;
        delete [] f3;
        delete [] f4;
        // delete [] y;
        delete [] x;
        delete [] f;

        return y;
    }

    
}

void __lorenz__(double x, double y[], double f[])
{
    double sigma = 10e0;
    double rho = 28e0;
    double beta = 8e0 / 3e0;

    f[0] = sigma * (y[1] - y[0]);
    f[1] = rho * y[0] - y[1] - y[0] * y[2];
    f[2] = y[0] * y[1] - beta * y[2];
}

int main(int argc, char const *argv[])
{
    double a = 0e0;
    double b = 100e0;
    double ht = 1e-5;
    int n = 3;
    double ivp[3] = {0e0, 1e0, 0e0};
    clock_t start, end;
    start = clock();
    Solver(a, b, ht, ivp, n, __lorenz__);
    end = clock();
    std::cout << "Time: " << (double)(end - start) / CLOCKS_PER_SEC << "s" << std::endl;

    return 0;
}
