# to call the command line
#
# ipython -c 'import stapleTests; print stapleTests.stapleTests(420,6)'
#
def stapleTests(totalStudents,PagsTest):
    s = ""
    for i in range(0,totalStudents):
        s=s+(str(i*PagsTest+1)+"-"+str((i+1)*PagsTest)+";")
    return s[:-1]
