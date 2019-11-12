#include <stdio.h> 
#include <cs50.h>
#include <math.h>

int main (void)
{
    
    float dollars; 
    do {dollars = get_float("change:");} 
        while (dollars < 0); 
    int cents = round(dollars * 100); 
    //make to be whole number integer
    // printf("%i\n", cents);
    
    //find the number of coins
    int n = cents / 25 + cents%25 / 10 + cents%25%10 / 5 + cents%25%10%5 / 1; 
    printf ("%i\n", n);
   
}
