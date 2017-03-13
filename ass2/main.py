#Time Stamping a document
#public key is (23,323) and private key is (263,323) : e = 23, d = 263, n = 323 - RSA Implementation
import hashlib
import datetime
public = (23,323)
def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]  #ord(c) : Given a string of length one, return an integer representing the Unicode code point of the character when the argument is a unicode object, or the value of the byte when the argument is an 8-bit string. For example, ord('a') returns the integer 97
    #Return the array of bytes
    return cipher

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)

def server(h):
	private = (263,323)
	a = str(datetime.datetime.now())
	b = hashlib.sha1(a).hexdigest()
	plaintext = h + b
	ciphertext= encrypt(private,plaintext)
	return ciphertext


def client():
	document="Python is a great language!!"
	print "Initial Document = "+document
	h = hashlib.sha1(document).hexdigest() #SHA1 of the document before it's sent to the time stamping server
	signature= server(h)
	plain = decrypt(public,signature)
	document=document+plain
	print "After Timestamping = "+document
	print "To verify if the document existed at that point of time"
	timest = document[-40:] #Timestamp
	hashdct =document[-80:-40] #SHA1 hash of the document
	textdct = document[:-80] # text of the document
	#compare the hash of the present text with the hash generated at the beginning.
	b = hashlib.sha1(textdct).hexdigest()
	if b == hashdct:
		print "Document is Verified"
	else:
		print "Document is Modified and Tampered"



client()