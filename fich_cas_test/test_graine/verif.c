#include <stdio.h>
#include <stdlib.h>

#define RESET   "\033[0m"         // Reset color
#define RED     "\033[31m"        // Red color
#define GREEN   "\033[32m"        // Green color
#define YELLOW  "\033[33m"        // Yellow color
#define BLUE    "\033[34m"        // Blue color

int main() {
    FILE *file1, *file2;
    char ch1, ch2;
    
    // Open the first file in read mode
    file1 = fopen("rez1.txt", "r");
    if (file1 == NULL) {
        perror("Error opening rez1");
        return 1;
    }
    
    // Open the second file in read mode
    file2 = fopen("rez2.txt", "r");
    if (file2 == NULL) {
        perror("Error opening rez2");
        fclose(file1);
        return 1;
    }
    
    // Compare each character in both files
    while ((ch1 = fgetc(file1)) != EOF && (ch2 = fgetc(file2)) != EOF) {
        if (ch1 != ch2) {
            printf(RED"\n /!\Error"RESET" : With the same root you have different results.\n \n");
            fclose(file1);
            fclose(file2);
            return 0;
        }
    }
    
    // Check if both files have reached EOF (end of file)
    if (fgetc(file1) == EOF && fgetc(file2) == EOF) {
        printf(GREEN"\n Nice!" RESET " You have the same results with the same 'graine'.\n \n");
    } else {
        printf("Not Good\n");
    }
    
    // Close the files
    fclose(file1);
    fclose(file2);
    
    return 0;
}

