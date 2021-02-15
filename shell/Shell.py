#! /usr/bin/env python3

import os, sys, time, re


while True:

    os.write(1, ("$ ").encode())

    command = os.read(0,1000)

    if re.split("[ \n]",command.decode())[0] == "exit":
        os.write(1, "exiting...\n".encode())
        sys.exit(0)
    
    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        args = re.split("[ \n]", command.decode())
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

    else:                           # parent (forked ok)
        os.wait()

