import rsa
SWC_KEY_LEN = 1024
def generatePrivateAndPublicKeys(user):
    if user == 'SWC':
      print('generating keys for SWC....please wait')
      pu, pr = rsa.newkeys(SWC_KEY_LEN)
    elif user == 'EC':
      print('generating keys for EC....please wait')
      pu, pr = rsa.newkeys(SWC_KEY_LEN*2)
    elif user == 'CC':
      print('generating keys for CC....please wait')
      pu, pr = rsa.newkeys(SWC_KEY_LEN*4)
    else:
      print('Invalid User. Try Again')
      getuser()
      return
  
    with open('private_key_' + user + '.pem', 'wb') as fw:
      fw.write(pr.save_pkcs1('PEM'))

    with open('public_key_' + user + '.pem', 'wb') as fw:
      fw.write(pu.save_pkcs1('PEM'))

def getuser():
  useri = input("Enter the user : ")
  generatePrivateAndPublicKeys(useri)

getuser()