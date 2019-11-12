#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
//checks if argument count equals 2. If not reprompt.{  
{
    if (argc == 2)
    {
        for (int i = 0; i < strlen(argv[1]); i++) 
            //check if every character is a number. If bigger or smaller than 0-9 it's not a number
        {
            if (argv[1][i] < '0' || argv[1][i] > '9')//reprompt and end if not a number.
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        int n = atoi(argv[1]); 
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1; 
    }
    //get a text from user to encrypt 
    int n = atoi(argv[1]);
    string s = get_string("Plaintext: "); 
    printf("Cyphertext: "); 
    
    //transfer string characters into number in ASCII format!!!
    for (int i = 0; i < strlen(s); i++)
    {
        if((int) s[i] >= 97 && s[i] <= 122)
        {
            //adding (int) automatically turn a character into ASCII form. bruh I should of know that earlier.
            char newVal = (s[i] + n - 97) % 26 +97; 
            printf("%c", newVal); 
        }
        else if (s[i] >= 65 && s[i] <= 90)
        {
            char newVal = (s[i] + n - 65) % 26 + 65; 
            printf("%c", newVal);
        }        
        else 
        {
            printf("%c", s[i]); 
        }
    }
    printf("\n"); 
    
}
    

