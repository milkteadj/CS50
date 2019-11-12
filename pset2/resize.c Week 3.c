// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    //check if n is a number
    for (int nlen = 0, len = strlen(argv[1]); nlen < len; nlen++)
    {
        if (argv[1][nlen] < '0' || argv[1][nlen] > '9')
        {
            printf("n has to be a number\n");
            return 1;
        }
    }

    //set n from user input
    int n = atoi(argv[1]);

    //if n bigger than 100 or smaller than 0, reprompt
    if (n > 100 || n <= 0)
    {
        fprintf(stderr, "Resize value must be between 0 and 100\n");

        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER and set outfile BITMAPHEADERFILE equal to it.
    BITMAPFILEHEADER bf, bfRe;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    bfRe = bf;

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi, biRe;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    biRe = bi;

    //set the outfile header files to adjust by resize value
    biRe.biWidth = bi.biWidth * n;
    biRe.biHeight = bi.biHeight * n;

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for scanlines for infile and outfile
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int outpadding = (4 - (biRe.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // New file and image size
    bfRe.bfSize = 54 + biRe.biWidth * abs(biRe.biHeight) * 3 + abs(biRe.biHeight) * outpadding;
    biRe.biSizeImage = ((biRe.biWidth * 3) + outpadding) * abs(biRe.biHeight);
    //biRe.biSizeImage = ((((biRe.biWidth * biRe.biBitCount) + 31) & ~31) / 8) * abs(biRe.biHeight);

    // write outfile's BITMAPFILEHEADER. Same size, 14 bytes.
    fwrite(&bfRe, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER. It will be the same size, 40 bytes.
    fwrite(&biRe, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        //vertically add additional rows
        for (int row_count = 0; row_count < n; row_count++)
        {

            // iterate over pixels in scanline //for each row
            for (int j = 0; j < bi.biWidth; j++)
            {
                // temporary storage
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                //for n times
                for (int count = 0; count < n; count++)
                {
                    // write RGB triple to outfile
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add padding
            for (int k = 0; k < outpadding; k++)
            {
                fputc(0x00, outptr);
            }

            //brings cursor back n-1 times
            if (row_count < n - 1)
            {
                fseek(inptr, -(bi.biWidth) * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
