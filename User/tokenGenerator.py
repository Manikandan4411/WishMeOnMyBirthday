def createToken(user):
  return user.username+user.password


def checkToken(user, token):
  local_token = user.username+user.password
  if(local_token == token):
    return True
  else:
    return False