#import config 

#config.write_environ()
#config.read_environ()

import config
config.write_environ()

import databaseIO

def add():
    databaseIO.auth_adduser("123456789","asdf-asdf","asdf",12)
    return

def check():
    at,ats,delete_time=databaseIO.auth_checkuser("123456789")
    print("{}, {}, {}".format(at,ats,delete_time))
    return

def deleteuser():
    databaseIO.auth_deleteuser("123456789")
    return

def deleteall():
    databaseIO.auth_deleteall()
    return

def drop():
    databaseIO.auth_drop()
    return

def get():
    print(databaseIO.auth_getalluser())
    return


#add()

#get()

drop()
