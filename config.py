username=''
password=''
secret=''
enctoken=None

try:
    enctoken = open('enctoken.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    enctoken = None
