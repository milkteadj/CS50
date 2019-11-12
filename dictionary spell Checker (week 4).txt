// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

//initialize counter
int counter = 0;
int *ip = &counter;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }
    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        //TODO
        //malloc space
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            unload();
            return false;
        }
        //add to word counter
        *ip = *ip + 1;

        //set word into new node
        strcpy(new_node->word, word);

        //run through hash function and get hashcode
        int hashcode = hash(word);

        //check if pointer of that hash function is null. If null, make it point to this.
        if (hashtable[hashcode] == NULL)
        {
            hashtable[hashcode] = new_node;
            new_node->next = NULL;
        }
        //if node already in that hashcode
        else if(hashtable[hashcode] != NULL)
        {
            //set new node to point to the header
            node *header = hashtable[hashcode];
            new_node->next = header;

            //set hashtable pointer to point to the new node
            hashtable[hashcode] = new_node;
        }
    }
    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    for (int i = 0; i < 26; i++)
    {
        if (hashtable[i] == NULL)
        return 0;
    }
    return *ip;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    //check for which link list in the hash table
    int hashcode = hash(word);
    node *cursor = hashtable[hashcode];
    while(cursor != NULL)
    {
        char *LowerWord = malloc(sizeof(word) + 4);
        if (LowerWord == NULL)
        {
            return false;
        }
        for (int i = 0; i < strlen(word); i++)
        {
            LowerWord[i]= tolower(word[i]);
        }
        //this was the problem area...
        LowerWord[strlen(word)] = '\0';
        //make it not case sensitive. Compare the two strings.
        if(strcmp(LowerWord, cursor->word) == 0)
        {
            free(LowerWord);
            return true;
        }
        else
        {
            free(LowerWord);
            //move on to the next word in the hashtable and check
            cursor = cursor->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    //repeat 26 times for the whole hashtable
    for (int i = 0; i < 26; i++)
    {
        //set cursor to the header of each link list in hashtable
        node *cursor = hashtable[i];
        //if not at the end of LL, free each node
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;

}
