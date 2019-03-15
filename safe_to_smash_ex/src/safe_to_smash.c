#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>


typedef struct feature {
    char* description;
    struct feature* next;
} feature_t;

feature_t* head = 0;

void add_feature(char* desc){
    if(!getenv("DEBUG")) printf("[!] Adding feature '%s' (at %p)\n", desc, desc);
    feature_t* f = (feature_t*)malloc(sizeof(feature_t));
    f->description = desc;
    f->next = head;
    head = f;
}

void print_features(){
    feature_t* ptr = head;
    printf("We got a lot of security features! This binary is unexploitable :D \n");
    while(ptr != 0){
        printf("[!] %s\n", ptr->description);
        ptr = ptr->next;
    }
}

void user_feature(){
    int64_t N = 255;
    char feature[N];

    printf("Which feature do you want us to add?\n");
    fflush(stdout);
    scanf("%s", feature);

    printf("For additional security please enter the string length of your feature:\n");
    fflush(stdout);
    scanf("%lld", &N);
    
    char* f = malloc(strlen(feature)-1);
    if(f) strncpy(f, feature, N);

    if(!getenv("DEBUG")) printf("[!] Old string terminator is: %c\n", f[N]);
    if(f) f[N] = feature[N];

    if(f) add_feature(f);
    printf("Nice!\n");

    print_features();
}


int64_t main(){
    char f1[255] = "The stack IS NOT executable";
    char f2[255] = "ASLR is enabled";
    char f3[255] = "PIE is enabled";
    char f4[255] = "Canaries are enabled";

    add_feature(f1);
    add_feature(f2);
    add_feature(f3);
    add_feature(f4);
    
    print_features();
    
    char ans[255];
    printf("Don't you think so? ");

    printf("Do you want to add a feature (yes/no)?\n");
    fflush(stdout);
    scanf("%s", ans);
    while (strcmp(ans, "yes") == 0){
        user_feature();
        printf("Do you want to add a feature (yes/no)?\n");
        fflush(stdout);
        scanf("%s", ans);
    }
}