#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;
    char str[100];
    int part1 = 0, part2 = 0;
 
    fp = fopen("inputs/1", "r");
    while(fgets(str, sizeof(str), fp) != NULL) {
        int first = -1, last = -1, index = 0;
        int p2first = -1, p2last = -1;
        
        // just brute force parsing
        while(str[index] != 0) {

            if(str[index] >= '0' && str[index] <= '9') {
                if(first == -1)
                    first = str[index] - '0';
                if(p2first == -1) 
                    p2first = first;
                last = str[index] - '0';
                p2last = last;
            } else {
                switch(str[index]) {
                    case 'o':
                        if(str[index+1] == 'n' && str[index+2] == 'e') {
                            if(p2first == -1)
                                p2first = 1;
                            p2last = 1;
                        }
                        break;
                    case 't':
                        if(str[index+1] == 'w' && str[index+2] == 'o') {
                            if(p2first == -1)
                                p2first = 2;
                            p2last = 2;
                        } else if(str[index+1] == 'h' && str[index+2] == 'r' && 
                                  str[index+3] == 'e' && str[index+4] == 'e'){
                            if(p2first == -1)
                                p2first = 3;
                            p2last = 3;
                        }
                    case 'f':
                        if(str[index+1] == 'o' && str[index+2] == 'u' && str[index+3] == 'r') {
                            if(p2first == -1)
                                p2first = 4;
                            p2last = 4;
                        } else if(str[index+1] == 'i' && str[index+2] == 'v' && 
                                  str[index+3] == 'e') {
                            if(p2first == -1)
                                p2first = 5;
                            p2last = 5;
                        }
                        break;
                    case 's':
                        if(str[index+1] == 'e' && str[index+2] == 'v' &&
                           str[index+3] == 'e' && str[index+4] == 'n') {
                            if(p2first == -1)
                                p2first = 7;
                            p2last = 7;
                        } else if(str[index+1] == 'i' && str[index+2] == 'x') {
                            if(p2first == -1)
                                p2first = 6;
                            p2last = 6;
                        }
                        break;
                    case 'e':
                        if(str[index+1] == 'i' && str[index+2] == 'g' &&
                           str[index+3] == 'h' && str[index+4] == 't') {
                            if(p2first == -1)
                                p2first = 8;
                            p2last = 8;
                        }
                        break;
                    case 'n':
                        if(str[index+1] == 'i' && str[index+2] == 'n' && str[index+3] == 'e') {
                            if(p2first == -1)
                                p2first = 9;
                            p2last = 9;
                        }
                        break;
                }
            }
            index++;
        }
        part1 += first * 10 + last;
        part2 += p2first * 10 + p2last;

    }
    fclose(fp);
    printf("Part 1: %d\nPart 2: %d\n", part1, part2);
    
    return 0;
}
