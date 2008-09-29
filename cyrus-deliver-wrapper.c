/*
 * Wrapper for cyrus 'deliver' to allow anyone to run it -
 * I hope this is secure!  Should be setgid mail.
 */

#include <stdio.h>
#include <unistd.h>
#include <pwd.h>
#include <sys/types.h>
#include <sysexits.h>

#ifndef LIBEXECDIR
#define LIBEXECDIR "/usr/libexec/cyrus"
#endif

int main(int argc, char *argv[])
{
    char *const envp[] = { NULL };
    struct passwd *ent = getpwuid(getuid());
    const char *uname = (ent && ent->pw_name && ent->pw_name[0])
                              ? ent->pw_name : "anonymous";
    
    if (argc != 2) {
        fprintf(stderr, "Usage: %s mailbox\n", argv[0]);
        return EX_USAGE; 
    }
    
    execle(LIBEXECDIR"/deliver", "deliver", "-e",
           "-a", uname, "-m", argv[1],
           NULL, envp);

    perror("exec "LIBEXECDIR"/deliver");           
    return EX_OSERR; 
}
