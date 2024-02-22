#include <windows.h>
#include <stdio.h>

int main
(void)
{
    // Test the modified shellcode to load something
    FILE* fd = fopen("ldlib.bin", "rb");
    fseek(fd, 0, SEEK_END);
    unsigned long size = ftell(fd);
    rewind(fd);

    unsigned char* shellcode = malloc(size);
    if (fread(shellcode, size, 1, fd) != size)
    {
        fclose(fd);
    }

    // M
   buffer[147] = 0x4d;
   // a 
   buffer[482] = 0x61;
   // g -> input - 3 -> d -> a
   buffer[474] = 0x64;
   // i
   buffer[483] = 0x69;
   // c -> input - 2 -> a
   buffer[485] = 0x61;

    unsigned long old_protections;
    VirtualProtect(shellcode, size, PAGE_EXECUTE_READWRITE, &old_protections);
    HANDLE h_thread = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)shellcode, 0, 0, 0);
    if (h_thread)
    {
        WaitForSingleObject(h_thread, INFINITE);
    }
    return 0;
}