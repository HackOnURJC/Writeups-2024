#include <windows.h>
#include <stdio.h>

int main
(void)
{

    FILE* fd = fopen("ciphered.dll", "rb");
    if (fd == NULL)
    {
        printf("Failed to open the dll");
        return 1;
    }

    fseek(fd, 0, SEEK_END);
    unsigned long size = ftell(fd);
    rewind(fd);

    unsigned char* buffer = VirtualAlloc(0, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (buffer == NULL)
    {
        printf("Failed to alloc space");
        return 1;
    }

    if (fread(buffer, 1, size, fd) != size)
    {
        fclose(fd);
    }

    char d, zero, n, eight, r, u, T, three, comma, t, h, one, k;

    printf("%c", buffer[191644]);
    printf("%c", buffer[74980]);
    printf("%c", buffer[93606]);
    printf("%c", buffer[125565]);
    printf("%c", buffer[100452]);
    printf("%c", buffer[120684]);
    printf("%c", buffer[106950]);
    printf("%c", buffer[106775]);
    printf("%c", buffer[83201]);
    printf("%c", buffer[78179]);
    printf("%c", buffer[96450]);
    printf("%c", buffer[80201]);
    printf("%c", buffer[69997]);
    printf("%c", buffer[72694]);
    printf("%c", buffer[64553]);
    printf("%c", buffer[60540]);
    return 0;
}
