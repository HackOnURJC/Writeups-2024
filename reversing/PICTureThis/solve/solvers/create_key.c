#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

char pin[] = "17022024";

/*
    Function to swap 2 values
*/
void swap(char* a, char* b) {
    char temp = *a;
    *a = *b;
    *b = temp;
}

/*
    Permutate the dictionary based on the PIN code provided (matched day played)
*/
void recoverAESIV
(char* dictionary) 
{
    int year = (pin[6] - '0') * 10 + (pin[7] - '0');
    int len = strlen(dictionary);

    int year_month = year - (pin[3] - '0');

    // Swap based on pincode
    swap(&dictionary[pin[0] - 'a'], &dictionary[year % len]);
    swap(&dictionary[pin[3] - 'a'], &dictionary[0]);

    // Perform rotation -1 (substract 1)
    for (int i = 0; i < len; i++) {
        dictionary[i] = (dictionary[i] - 'a' - 1 + 26) % 26 + 'a';
    }

    // Perform rotation 24 (add 24)
    for (int i = 0; i < len; i++) {
        dictionary[i] = (dictionary[i] - 'a' + 24) % 26 + 'a';
    }

    // Perform XOR operation with the hardcoded value "mewing"
    char* key = "mewing";
    int key_len = strlen(key);
    for (int i = 0; i < len; i++) {
        dictionary[i] ^= key[i % key_len];
        if (!isprint(dictionary[i])) { // Check if the result is not printable
            // Modifying non-printable characters to be printable
            dictionary[i] = (dictionary[i] % 94) + 33; // Ensuring the result is in printable ASCII range
        }
    }

    // Perform rotation 33 (add 33)
    for (int i = 20; i < len; i++) {
        dictionary[i] = (dictionary[i] - 'a' + 33) % 26 + 'a';
    }


    // Perform rotation 33 (add 33)
    for (int i = 0; i < 20; i++) {
        dictionary[i] = (dictionary[i] - 'a' - 33) % 26 + 'a';
    }

    recoverIV(dictionary);
}

void recoverIV
(char* dictionary)
{
    char* dict = "abcdefghijklmnopqrstuvwxyz";

    char reconstructed_iv[17];                      // Allocate space for the reconstructed IV
    reconstructed_iv[0] = '_';                      // hardcoded _
    reconstructed_iv[1] = dictionary[16] +32;       // n from dict tolower
    reconstructed_iv[2] = pin[0];                   // 1st digit of PIN (1)
    reconstructed_iv[3] = dictionary[20] + 6;       // g from dict
    reconstructed_iv[4] = dictionary[19] + 32;      // H from dict tolower
    reconstructed_iv[5] = dictionary[29] + 32;      // T from dict tolower
    reconstructed_iv[6] = '_';                      // hardcoded _
    reconstructed_iv[7] = dictionary[29] + 32;      // T from dict tolower
    reconstructed_iv[8] = dictionary[19] + 32;      // H from dict tolower
    reconstructed_iv[9] = pin[2];                   // 3rd digit of PIN (0)
    reconstructed_iv[10] = '?';               // u from dict
    reconstructed_iv[11] = dictionary[20] + 6;      // g from dict
    reconstructed_iv[12] = dictionary[19] + 32;     // H from dict tolower
    reconstructed_iv[13] = dictionary[29] + 32;     // T from dict tolower
    reconstructed_iv[14] = '?';               // s from dict
    reconstructed_iv[15] = '_';                     // hardcoded
    reconstructed_iv[16] = '\0';                    // Null-terminate the string

    for (size_t i = 0; i < 27; i++)
    {
        for (size_t j = 0; j < 27; j++)
        {
            reconstructed_iv[10] = dict[i];
            reconstructed_iv[14] = dict[j];
            // Searching manually on the results:
            if (dict[i] == 'u' && dict[j] == 's')
            {
                printf("Recovered AES IV:%s\n", reconstructed_iv);
            }
            
        }
    }
}

char* recoverAESKey
(char* dictionary)
{
    // Define the indices of the characters needed for the string
    int indices[] = {19, 7, 53, 18, -1, 12, 5, -1, 2, 19, 5, -1, 3, 17, 53, 21, 55, 18, -1, 12, 55, -1, 10, 10, 17, 56, 25, 24, -1, 52, -1, 52};

    // Initialize an empty string to store the result
    char* result = malloc(33);

    // Loop through the indices to retrieve characters from the dictionary
    for (size_t i = 0; i < 33; i++) {
        if (i < 32)
        {
            if (indices[i] != -1) 
            {
                result[i] = dictionary[indices[i]];
            } else 
            {
                if (i == 30)
                {
                    result[i] = '.';
                }
                else
                {
                    result[i] = '_';    
                }
            }
        }
        else
        {
            result[i] = '\0';
        }
        
    }

    printf("Recovered AES key: %s\n", result);

}

int main() {
    // Define the dictionary
    char dictionary[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    // Recover AES key
    recoverAESKey(dictionary);
    // Print the result


    // Permutate the dictionary based on the pincode and generate IV
    recoverAESIV(dictionary);

    return 0;
}
