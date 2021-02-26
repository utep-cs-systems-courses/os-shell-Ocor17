#! /usr/bin/env python3

import os, sys, time, re

def execve(args):    
        #print("-------------",args)
        for dir in re.split(":", os.environ['PATH']): # try each directory in the path
            program = "%s/%s" % (dir, args[0])
            #os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, args, os.environ) # try to exec program
            except FileNotFoundError:             # ...expected
                pass                              # ...fail quietly

        os.write(2, ("Could not exec %s\n" % args[0]).encode())
        sys.exit(1)                 # terminate with error

p_read, p_write = os.pipe()

PS1 ="$ "
if ((os.environ.get('PS1'))!= None):
    PS1 = os.environ.get('PS1') 

for f in (p_read, p_write):
    os.set_inheritable(f, True)

while True:

    if in_pipe == False:
        os.write(1, ((os.getcwd()+(PS1)).encode()))
        command = os.read(0,1000)
        args = re.split("[ \n]", command.decode())

    if args[0] == "exit":
        os.write(1, "exiting...\n".encode())
        sys.exit(0)

    if args[0] == "cd":
        if(args[1]!=None):
            try:
                os.chdir(args[1])
                continue
            except FileNotFoundError:
                os.write(2, ("Directory does not exist %s\n" % args[1]).encode())
                continue

    
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        if '>' in args:
            os.close(1)
            os.open(args[args.index('>')+1], os.O_CREAT | os.O_WRONLY); #create file to write to
            os.set_inheritable(1,True) # > needs display fd
            args.remove(args[args.index('>')+1]) #prep for more
            args.remove('>')

        if '<' in args:
            os.close(0)
            os.open(args[args.index('<')+1], os.O_RDONLY)
            os.set_inheritable(0,True) # < needs keyboard fd
            args.remove(args[args.index('<')+1])
            args.remove('<')

        if '|' in args:
            os.close(1)
            os.set_inheritable(os.dup(p_write),True)
            args = args[:args.index('|')] #seperate pipes to get ready to handle them sequentially
            for fd in (p_read,p_write):
                os.close(fd)

        execve(args)

    else:                           # parent (forked ok)
        os.wait()

