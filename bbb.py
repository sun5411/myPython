#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pexpect
import commands,os,sys
import pdb

if __name__ == '__main__':
    user = 'sun'
    ip = '127.0.0.1'
    mypassword = 'oracle'

    #pdb.set_trace()
    child = pexpect.spawn('ssh %s@%s' % (user,ip))
    child.expect ('password')
    child.sendline (mypassword)

    child.expect('$')
    print child.before
    child.sendline('pidof ntpd')
    child.expect("[:]")
    child.sendline(mypassword)
    child.expect('$')
    print "before :"
    print child.before
    child.sendline("echo '112' >> ~/1.txt")
    #child.interact()

    pass
