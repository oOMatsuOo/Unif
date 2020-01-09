#include <stdio.h>
#include <assert.h>
#include <stdlib.h>


int main(int argc, char **argv){

    assert(argc == 4);

    int a = atoi(argv[1]), b = atoi(argv[3]), result;

    if (argv[2][0] == 'x')
        result = a * b;

    else if (argv[2][0] == '+')
        result = a + b;

    else if (argv[2][0] == '/')
        result = a / b;

    else if (argv[2][0] == '-')
        result = a - b;

    printf("%d * %d = %d \n", a, b, result);
   
    return 0;

}