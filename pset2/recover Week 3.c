#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    //user should provide name of the file in command line.
    if (argc != 2)
    {
        fprintf(stderr, "Please provide the name of the file to recover\n");
        return 1;
    }

    //name the file of argv[1]
    char *file = argv[1];

    //open file. If cannot, return 2
    FILE *openf = fopen(file, "r");
    if (openf == NULL)
    {
        fprintf(stderr, "Cannot open %s\n", file);
        return 2;
    }

    //initial variables
    char filename[8];
    int picnum = 0;
    BYTE buffer[512];
    int foundpic = 0; //0 is not found, 1 + is found.
    FILE *img = NULL;

    //repeat reading the buffer chunks until the end
    while (fread(&buffer, sizeof(buffer), 1, openf) == 1)
    {
        //start of a new jpeg?
        if (foundpic == 0)
        {
            //yes
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
            {
                foundpic++;
                //open new picture file
                sprintf(filename, "%03i.jpg", picnum);
                img = fopen(filename, "w");
                fwrite(&buffer, 512, 1, img);

            }
            //no -> do nothing
        }

        //already found a JPEG
        else
        {
            //yes
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff)
            {
                //stop last pic file
                fclose(img);

                //open new pic file
                picnum++;
                sprintf(filename, "%03i.jpg", picnum);
                img = fopen(filename, "w");
                fwrite(&buffer, 512, 1, img);
            }
            //no new one
            else
            {
                fwrite(&buffer, 512, 1, img);
            }

        }
    }

    //if at the end buffer of the file
    if (fread(&buffer, sizeof(buffer), 1, openf) != 1)
    {
        fwrite(&buffer, 1, 512, img);
    }
    printf("JPEG count: %i\n", picnum);

    fclose(img);
    fclose(openf);
}
