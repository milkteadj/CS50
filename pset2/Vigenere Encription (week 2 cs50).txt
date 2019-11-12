#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int shift(char c); 

int main(int argc, string argv[])
//checks if argument count equals 2. If not reprompt.{  
{
    if (argc == 2)
    {
        for (int i = 0; i < strlen(argv[1]); i++) 
            //check if every character is a number. If bigger or smaller than 0-9 it's not a number
        {
            if (argv[1][i] < 65 || argv[1][i] > 122)//reprompt and end if not a number.
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
            else if (argv[1][i] > 90 && argv[1][i] < 97)
            {
                printf("Usage: ./vigenere keyword\n"); 
                return 1; 
            }
        }
    }
    else
    {
        printf("Usage: ./vigenere keyword\n");
        return 1; 
    }
    //get a text from user to encrypt 
    string s = get_string("Plaintext: "); 
    printf("ciphertext: "); 
    //initial k is set to 0. 
    int k = 0; 
    //transfer string characters into number in ASCII format!!!
    for (int i = 0; i < strlen(s); i++)
    {
        //adds to variable k if a character is not a letter. 
        if (isalpha(s[i]) == 0)
        {
            k++;     
        }
        //if i ever gets big, j will always repeat this way because it's a remainder. 
        int j = (i - k) % strlen(argv[1]); 
        
        //if lower case
        if ((int) s[i] >= 97 && s[i] <= 122)
        {
            //adding (int) automatically turn a character into ASCII form. 
            char newVal = (s[i] + shift(argv[1][j]) - 97) % 26 + 97; 
            printf("%c", newVal); 
        }
        //if upper case
        else if (s[i] >= 65 && s[i] <= 90)
        {
            char newVal = (s[i] + shift(argv[1][j]) - 65) % 26 + 65; 
            printf("%c", newVal);
        }   
        //if not lower or upper (not a letter), then print the original character. 
        else 
        {
            printf("%c", s[i]); 
        }
    }
    printf("\n"); 
    
}

//shift the lower and upper letters of the keywords into keys. A or a is 0, and Z or z is 25. 
int shift(char c)
{
    if (c >= 97 && c <= 122)
    {
        c = c  - 97; 
    }
    if (c >= 65 && c <= 90) 
    {
        c = c - 65;
    } 
    return c;
      
}
    
