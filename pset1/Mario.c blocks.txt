#include <cs50.h>
#include <stdio.h>

int main(void)
   
{ 
   int n;
   do {n = get_int("Height(1-8):");}
    while(n<1 || n>8);
char *m ="\n";
    
    if(n== 1){
    m = ("#\n");}
else if(n ==2){
    m = (" #\n##\n");
}
else if(n ==3){
    m =("  #\n ##\n###\n"); 
}
else if(n ==4){
    m = ("   #\n  ##\n ###\n####\n");
}
else if(n ==5){
    m = ("    #\n   #\n  ###\n ####\n#####\n"); 
}
else if(n ==6){
    m = ("     #\n    ##\n   ###\n  ####\n #####\n######\n");
}
else if(n ==7){
    m = ("      #\n     ##\n    ###\n   ####\n  #####\n ######\n#######\n");
}
else if(n ==8){
    m = ("       #\n      ##\n     ###\n    ####\n   #####\n  ######\n #######\n########\n");
}

  printf("height: %i\n%s", n, m);
} 
