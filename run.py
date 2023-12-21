import os
import sys

## change to parent directory (from libEmailLog to src)
os.chdir('../')

from email_log import run

if __name__ =="__main__":
    
    run()
