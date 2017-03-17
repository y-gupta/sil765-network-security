#Time Stamping a document
#public key is (23,323) and private key is (263,323) : e = 23, d = 263, n = 323 - RSA Implementation


import hashlib
import datetime
import struct

public = (65537,5551201688147)
# private = (109182490673,5551201688147)
# n is 43 bit number - split m into 40-bit blocks, and obtain 43-bit encrypted message. pad 43 bits to 48 in output for convienience.


def hex_repr(str):
  return " ".join("%02x" % ord(b) for b in str)

def encrypt(pk, plaintext):
  #Unpack the key into it's components
  key, n = pk

  cipher = ""

  for i in xrange(0,len(plaintext),5):
    block = plaintext[i:i+5]

    m = 0
    for i in range(len(block)):
      m = (m << 8) | ord(block[i])
    # m is exactly 40 bits long

    c = pow(m, key, n)
    # c is around 43 bits in size (to be padded to 48 bits)

    cipher_block = ""
    for i in range(6):
      cipher_block += chr((c & (255<<40)) >> 40)
      c = c << 8
    # block is exactly 6 bytes long

    cipher += cipher_block
    # print(hex_repr(block),hex_repr(cipher_block))

  return cipher

def decrypt(pk, ciphertext):
  #Unpack the key into its components
  key, n = pk

  plain = ""

  for i in xrange(0,len(ciphertext),6):
    cipher_block = ciphertext[i:i+6]
    c = 0
    for i in range(len(cipher_block)):
      c = (c << 8) | ord(cipher_block[i])
    # c is 43 bits long

    m = pow(c, key, n)
    # m is exactly 40 bits long

    plain_block = ""
    for i in range(5):
      plain_block += chr((m & (255<<32)) >> 32)
      m = m << 8
    # plain_block is exactly 5 bytes long

    # print(hex_repr(cipher_block),hex_repr(plain_block))
    plain += plain_block

  return plain

def server(h):
  private = (109182490673,5551201688147)
  timestamp = str(datetime.datetime.utcnow()) # length of timestamp is 26 characters
  hash = hashlib.sha1(h + timestamp).hexdigest()
  signature = encrypt(private, hash)
  return timestamp, signature


def client():
  src_fname="test.txt"
  tar_fname="signed.txt"

  # fo=open(src_fname, "w")
  # fo.write("Python is a great language.\nYeah its great!!\n");
  # fo.close()
  #Initial Document
  fs = open(src_fname,"r")
  document = fs.read()
  fs.close()
  print "Initial Document = "+ repr(document)


  h = hashlib.sha1(document).hexdigest() #SHA1 of the document before it's sent to the time stamping server

  timestamp,signature = server(h)
  print "Timestamp = " + timestamp
  print "Signature (in hex) = " + hex_repr(signature)

  ft=open(tar_fname, "w")
  ft.write(document);
  ft.write(timestamp);
  ft.write(signature);
  ft.close()


  #After Timestamping Document
  ft = open(tar_fname,"r")
  signed_doc = ft.read()
  ft.close()

  original_doc = signed_doc[0:-74]
  timestamp = signed_doc[-74:-48]
  signature = signed_doc[-48:] #signature written by the server

  print "\nVerifying if the document existed at timestamp = " + timestamp

  expected_hash = decrypt(public, signature)
  #compare the hash of the present text with the hash generated at the beginning.
  doc_hash = hashlib.sha1(original_doc).hexdigest()
  actual_hash =  hashlib.sha1(doc_hash + timestamp).hexdigest()

  print "Expected hash: "+repr(expected_hash)
  print "Actual hash: "+repr(actual_hash)

  if actual_hash == expected_hash:
    print "Document is Verified"
  else:
    print "Document is Modified and Tampered"

client()