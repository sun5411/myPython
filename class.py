#!/usr/bin/python

class People:
    name = "ren"
    high = "tall as a men"
    wight = "wight as a men"
    __money = "10 RMB"

    @classmethod
    def run(self):
        print "running..."
        print self.__money

    @staticmethod
    def test():
        print "static method test"
    #tr = classmethod(run)
    #tr = staticmethod(test)

if __name__=="__main__":
    sun=People()
    sun.name="sun ning"
    sun.money="1000"
    #print sun.run()
    print People.run()
    print People.test()
