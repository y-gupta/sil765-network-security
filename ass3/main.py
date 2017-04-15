import hmac
from hashlib import md5
import random
import math
q=227 #prime number
a=56 #primitive root
key = 'HAHGDSHHHKMYKEY' #secret key for HMAC

def start():
	global xa
	xa = random.randint(1,q) #private key of A: xa<q-1
	ya = modexp(a,xa,q) #ya=a^xa mod q
	print "Prime number q = "+str(q)
	print "Primitive root of "+str(q)+" = "+str(a)
	print "Public Key of A = "+str(ya)

	#Man in the Middle Attack Prevention
	print "Man in the Middle Attack Prevention Measure at A's end"
	h = hmac.new(key,'',md5)
	h.update(str(ya))

	## Merge with HMAC digest
	print "HMAC before sending to Client B = "+str(h.hexdigest())
	ya1 = str(ya)+str(h.hexdigest())	
	clientB(ya1)


def clientB(ya1):
	ya=int(ya1[:-32])
	print "Check for MITM attack at B's end"
	h1 = hmac.new(key,'',md5)
	h1.update(str(ya))
	u1 = str(h1.hexdigest())
	if u1 == str(ya1[-32:]):
		print "Result: No MITM Attack"
	else:
		print "MITM Attack."
		return
	xb = random.randint(1,q) #private key of B: xb<q-1
	message="hello 1"
	print "Message to be sent from B to A = "+message
	z = encode(message) #encoded message

	#cipher_pairs list will hold pairs (yb, d) corresponding to each integer in z
	cipher_pairs = []
	#i is an integer in z
	for i in z:
			xb = random.randint(1,q) #private key of B: xb<q-1
			yb = modexp(a,xb,q) #yb=a^xb mod q (public key of B)
			d = (i*modexp(ya,xb,q)) % q #(K=ya^xb mod q), d = KM mod q
			#add the pair to the cipher pairs list
			cipher_pairs.append( [yb, d] )

	encryptedStr = ""
	for pair in cipher_pairs:
			encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
	clientA(encryptedStr)

def clientA(cipher):
	plaintext = []
	print "Cipher Text received by A = "+cipher
	cipherArray = cipher.split()
	if (not len(cipherArray) % 2 == 0):
			return "Malformed Cipher Text"
	for i in range(0, len(cipherArray), 2):
			#c = first number in pair
			c = int(cipherArray[i])
			#d = second number in pair
			d = int(cipherArray[i+1])

			#s = c^x mod p
			s = modexp(c,xa,q)
			#plaintext integer = ds^-1 mod p
			plain = (d*modexp(s,q-2,q)) % q
			#add plain to list of plaintext integers
			plaintext.append(plain)

	decryptedText = decode(plaintext)

#remove trailing null bytes
	decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])

	print "decryptedText = "+decryptedText

#computes base^exp mod modulus
def modexp(base,exp,modulus):
		return pow(base, exp, modulus)

def encode(sPlaintext):
		byte_array = bytearray(sPlaintext, 'utf-8')
		iNumBits=8
		#z is the array of integers mod p
		z = []

		#each encoded integer will be a linear combination of k message bytes
		#k must be the number of bits in the prime divided by 8 because each
		#message byte is 8 bits long
		k = iNumBits//8

		#j marks the jth encoded integer
		#j will start at 0 but make it -k because j will be incremented during first iteration
		j = -1 * k
		#num is the summation of the message bytes
		num = 0
		#i iterates through byte array
		for i in range( len(byte_array) ):
				#if i is divisible by k, start a new encoded integer
				if i % k == 0:
						j += k
						num = 0
						z.append(0)
				#add the byte multiplied by 2 raised to a multiple of 8
				z[j//k] += byte_array[i]*(2**(8*(i%k)))

		#example
				#if n = 24, k = n / 8 = 3
				#z[0] = (summation from i = 0 to i = k)m[i]*(2^(8*i))
				#where m[i] is the ith message byte

		#return array of encoded integers
		return z

#decodes integers to the original message bytes
def decode(aiPlaintext):
		#bytes array will hold the decoded original message bytes
		bytes_array = []
		iNumBits=8
		#same deal as in the encode function.
		#each encoded integer is a linear combination of k message bytes
		#k must be the number of bits in the prime divided by 8 because each
		#message byte is 8 bits long
		k = iNumBits//8

		#num is an integer in list aiPlaintext
		for num in aiPlaintext:
				#get the k message bytes from the integer, i counts from 0 to k-1
				for i in range(k):
						#temporary integer
						temp = num
						#j goes from i+1 to k-1
						for j in range(i+1, k):
								#get remainder from dividing integer by 2^(8*j)
								temp = temp % (2**(8*j))
						#message byte representing a letter is equal to temp divided by 2^(8*i)
						letter = temp // (2**(8*i))
						#add the message byte letter to the byte array
						bytes_array.append(letter)
						#subtract the letter multiplied by the power of two from num so
						#so the next message byte can be found
						num = num - (letter*(2**(8*i)))

		#example
		#if "You" were encoded.
		#Letter        #ASCII
		#Y              89
		#o              111
		#u              117
		#if the encoded integer is 7696217 and k = 3
		#m[0] = 7696217 % 256 % 65536 / (2^(8*0)) = 89 = 'Y'
		#7696217 - (89 * (2^(8*0))) = 7696128
		#m[1] = 7696128 % 65536 / (2^(8*1)) = 111 = 'o'
		#7696128 - (111 * (2^(8*1))) = 7667712
		#m[2] = 7667712 / (2^(8*2)) = 117 = 'u'

		decodedText = bytearray(b for b in bytes_array).decode('utf-8')

		return decodedText


start()
