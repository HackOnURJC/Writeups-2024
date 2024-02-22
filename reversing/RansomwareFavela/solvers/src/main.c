#include <windows.h>
#include <wininet.h>
#include <stdio.h>
#include <dirent.h>
#include <stdlib.h>
#include "aes.h"

#define BUFFER_SIZE 512
#define MAX_WORDS 32
#define MAX_WORD_LENGTH 100

#define KEY_SIZE 32
#define IV_SIZE 16
#define MAX_WORD_LENGTH 100

BOOL PaddBuffer(IN PBYTE InputBuffer, IN SIZE_T InputBufferSize, OUT PBYTE* OutputPaddedBuffer, OUT SIZE_T* OutputPaddedSize) {

	PBYTE	PaddedBuffer        = NULL;
	SIZE_T	PaddedSize          = NULL;

	// calculate the nearest number that is multiple of 16 and saving it to PaddedSize
	PaddedSize = InputBufferSize + 16 - (InputBufferSize % 16);
	// allocating buffer of size "PaddedSize"
	PaddedBuffer = (PBYTE)HeapAlloc(GetProcessHeap(), 0, PaddedSize);
	if (!PaddedBuffer){
		return FALSE;
	}
	// cleaning the allocated buffer
	ZeroMemory(PaddedBuffer, PaddedSize);
	// copying old buffer to new padded buffer
	memcpy(PaddedBuffer, InputBuffer, InputBufferSize);
	//saving results :
	*OutputPaddedBuffer = PaddedBuffer;
	*OutputPaddedSize   = PaddedSize;

	return TRUE;
}

int main
(void)
{
    HINTERNET hInternet, hConnect, hRequest;
    BOOL bRet;
    DWORD bytesRead;
    char request_buffer[BUFFER_SIZE], aes_key[KEY_SIZE];
    char* token;
    int word_count = 0;
    int start_word = 28; // Starting word index
    int end_word = start_word + MAX_WORDS; // Ending word index

    // Open Internet connection
    hInternet = InternetOpen(NULL, INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (hInternet == NULL) {
        printf("Failed to open Internet connection\n");
        return 1;
    }

    // Connect to the server
    hConnect = InternetOpenUrl(hInternet, "https://gist.github.com/jsdario/6d6c69398cb0c73111e49f1218960f79/raw", NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (hConnect == NULL) {
        printf("Failed to connect to the server\n");
        InternetCloseHandle(hInternet);
        return 1;
    }

    InternetReadFile(hConnect, request_buffer, BUFFER_SIZE, &bytesRead);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);


    token = strtok(request_buffer, " \t\n");
    while (token != NULL && word_count < end_word) {
        // If word_count is greater than or equal to start_word, store the first character
        if (word_count >= start_word) {
            aes_key[word_count - start_word] = token[0];
        }
        word_count++;
        token = strtok(NULL, " \t\n");
    }

    printf("%d\n", word_count);

    unsigned char aes_iv[16] = {0x28, 0x39, 0x47, 0x28, 0x01, 0x44, 0x47, 0x28, 0x1a, 0x47, 0x1b, 0x46, 0x19, 0x47, 0x04, 0x28};
    
    for (size_t i = 0; i < 16; i++)
    {
        aes_iv[i] = aes_iv[i] ^ 0x777;
    }

    BYTE pKey[KEY_SIZE];
    BYTE pIv[IV_SIZE];

    // cipher
    struct AES_ctx ctx;
    // Copy AES key and IV byte by byte
    for (size_t i = 0; i < KEY_SIZE; i++) {
        pKey[i] = aes_key[i];
    }
    for (size_t i = 0; i < IV_SIZE; i++) {
        pIv[i] = aes_iv[i];
    }

	// Initializing the Tiny-AES Library
	AES_init_ctx_iv(&ctx, pKey, pIv);

    printf("iv:\n");
    for (size_t i = 0; i < 16; i++)
    {
        printf("%c, ", aes_iv[i]);
    }

    printf("\nkey:\n");
    for (size_t i = 0; i < 32; i++)
    {
        printf("%c", aes_key[i]);
    }
    printf("\n");
    printf("Opening flag.enc...\n");
    FILE *fd = fopen("flag.enc", "rb");
    if (fd == NULL)
    {
        printf("failed to open the flag");
    }


    fseek(fd, 0, SEEK_END);
    unsigned long size = ftell(fd);
    rewind(fd);


    unsigned char* buffer = (unsigned char*) malloc(size);
    if (fread(buffer, size, 1, fd) != size)
    {
        fclose(fd);
    }
    unsigned char* padded;
    size_t* padded_size;
    FILE* fp = fopen("flag.txt", "wb");
    if (buffer != NULL)
    {
        if (size % 16 != 0)
        {
            // Padding required, pad the buffer
            if (!PaddBuffer(buffer, size, &padded, &padded_size)) 
            {
                printf("Error padding buffer\n");
            }
            // Encrypting the padded buffer
            AES_CBC_decrypt_buffer(&ctx, padded, padded_size);
            
            fwrite(padded, padded_size, 1, fp);
            // Free memory for padded buffer
            HeapFree(GetProcessHeap(), 0, padded);
        }
        else
        {
            // No padding required, encrypt 'buffer' directly
            AES_CBC_decrypt_buffer(&ctx, buffer, size);
            fwrite(buffer, size, 1, fp);            
        }
    }
    
    unsigned char byte = 0x00;
    unsigned char byte2 = 0x0a;
    unsigned char byte3 = 0x09;
    unsigned char byte4 = 0x20;
    printf("%c%c%c%", byte, byte2, byte3, byte4);

    printf("result saved! -> flag.txt\n");
    return 0;
}