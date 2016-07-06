
import fa

def foo(what):
    if type(what) is str:
        print(what)
        return

    print('not a string')


bar = foo

bar('in c-fa.py')


##
cwd = '/tmp/a/b/c'
tmpfoo = fa.find(cwd, 'foo')


print(type(tmpfoo))
