from itsdangerous import TimedJSONWebSignatureSerializer

s = TimedJSONWebSignatureSerializer('123')
token = s.dumps("你好")
print(type(token), token)
token = token.decode()
print(type(token), token)
