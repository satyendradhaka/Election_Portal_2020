import rsa
SWC_KEY_LEN = 1024
def generatePrivateAndPublicKeys(user):
    if user == 'SWC':
      pu, pr = rsa.newkeys(SWC_KEY_LEN)
    elif user == 'EC':
      pu, pr = rsa.newkeys(SWC_KEY_LEN*2)
    elif user == 'CC':
      pu, pr = rsa.newkeys(SWC_KEY_LEN*4)
    else:
      print('Invalid User. Try Again')
      return
    
    with open('private_key_' + user + '.pem', 'wb') as fw:
      fw.write(pr.save_pkcs1('PEM'))

    with open('public_key_' + user + '.pem', 'wb') as fw:
      fw.write(pu.save_pkcs1('PEM'))


generatePrivateAndPublicKeys('SWC')
generatePrivateAndPublicKeys('EC')
generatePrivateAndPublicKeys('CC')