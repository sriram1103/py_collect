
class PrettyPrint():
    def __init__(self):
        self.sep = 100 * "-"
        self.one_sep = "\t"
        self.two_sep = self.one_sep * 2
        self.three_sep = self.one_sep * 3
        self.four_sep = self.one_sep * 4

    def fprint(self,dict):
        print self.sep
        print 

        #print dict
        for host in dict.keys():
            print "\t" + host
            print 
            host_data = dict[host]
            for section in host_data.keys():
                print "\t\t" + section
                print 
                for des,val in host_data[section].iteritems():
                    if '\n' in val:
                        print "\t\t\t" + des
                        for line in val.split('\n'):
                            print "\t\t\t\t" + line
                    else:
                        print "\t\t\t",
                        print "%-20s %s"%(des,val)

        print 
        print self.sep