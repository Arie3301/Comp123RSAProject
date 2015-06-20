#  Arie Slobbe, Noah Miannan, Duncan Claypool
# Comp 123
# Instructor: Elizabeth Ernst
# RSA Encryption program

#This program provides a means for secure, two way communication between parties running the same program. The program uses the RSA encryption method to convert ASCII sting messages ino sequences of integers. This encrypted message can only be decrypted with the correct private key associated with the public key that was used for encrytpion.



from random import randrange
from fractions import gcd
from tkinter import *


# Global Variables
p = 0
q = 0
n = 0
phi = 0
e = 0
d = 0
lst = [53,59,61,67,71,73] # from this list of prime numbers we generate our keys

# =========================================================================

# RSA related Functions

def findprime():
    """A helper function which takes no inputs. It chooses two random prime numbers from the global lst and produces an n and a phi(n) from those numbers."""
    
    #Global variables used by this function
    global phi
    global n
    global p
    global q
    
    # Generate two random integers
    lst1 = lst
    j = randrange(0,len(lst1))   
    k = randrange(0,len(lst1) - 1)  # Reduce the length of the string by one to account for the previous pop
    
    # Pick two prime numbers from the list by using the random integers as indexes
    p = lst1.pop(j)
    q = lst1.pop(k)
    n =  p * q
    phi = (p-1) * (q-1)

# the findprime() function was tested by running it several times. It returned (seemingly) random values from our list of prime numbers and it never returned the same prime number twice, as intended. 

def finde():
    """A helper function which takes no inputs. It finds the value e for the RSA encryption. e is used for encryption"""
    
    # Global variables used by this function
    global e
    global phi
    
    #Local Variables
    i = 0
    
    # Define e as the smallest number that is relatively prime to phi.     
    for x in range(3, phi, 2): 
        if i == 3:
            return
        if gcd(x,phi) == 1:
            e = x
            i += 1

# the finde() function was tested by running it several times with different p, q, and phi values. We confirmed by hand whether each time the value returned for e was indeed relatively prime to phi, which it always was.

def findd():
    """A helper function which takes no inputs. It finds the value d for the RSA encryption. d is used for decryption."""
    
    # Global variables used by this function    
    global d
    global e
    global phi
    
    # call a helper function to help determine the value of d
    (g,x,y) = egcd(e,phi)
    d = x % phi

# the findd() function was tested by running it several times with different p, q, and phi values. We confirmed by hand whether each time the value returned for d was indeed the multiplicative inverse of e mod(phi), which it always was.

def egcd(small,large):
    """This function executes the Euclidean greatest denominator algorithm which allows us to recursively find the greatest common denominator"""
    
    if small==0:
        return(large,0,1)
    else:
        (g,y,x) = egcd(large%small,small)
        return (g,x-(large//small)*y,y)

# the egcd() function is called by findd() and was tested along with that function. 

def findkeys():
    """Calls the functions findprime(), finde() and findd().  Upon startup, the GUI calls this function in order to generate the public and private keys."""
    
    findprime()
    finde()
    findd()

# the findkeys() function was tested by running it and checked by printing the values of the variables p, q, n, phi, d, and e, in the shell.

def encryption(msg):
    """ The encryption function. it takes an input message, encrypts it using the user's own public key, and returns a list of numbers that the decryption() function will accept.  """
    
    #Local Variables
    m = []
    c = []
    
    # converts msg into a list of ASCII numbers inside " m "
    for char in msg:
        value = ord(char)
        m.append(value)
    # Takes each item in list " m " and encrypts it by the following function:  " i = item^e mod(n) ". it then adds it to the encrypted list " c ".
    for item in m:
        i = pow(item,e,n)
        c.append(i)
    return c

# the encryption(msg) function was tested first by inserting small strings of characters whose ASCII values we were familiar with. After these tests were passed succesfully, we tested the encryption function with strings containing both the uppercase and lowercase alphabet as well as other standard US keyboard insertable symbols. The function was tested using different values of e and n as well. 

def theirEncryption(msg,theirE,theirN):
    """  The encryption function that uses the public key that has been provided by the user. It is called when the encrypt button in the GUI is pressed. It takes the input message and public key values (as two integers separated by a space). Returns a list of integer values. """
    
    #Local Variables
    m = []
    c = []
    
    # converts msg into a list of ASCII numbers inside " m "
    for char in msg:
        value = ord(char)
        m.append(value)
    # Takes each item in list " m " and encrypts it by the following function:  " i = item^e mod(n) ".  it then adds it to the encrypted list " c ".
    for item in m:
        i = pow(item,int(theirE),int(theirN))
        c.append(i)
    return c

# the theirEncryption(msg,theirE,theirN) function, which is very similar in functionality as the encryption() function, was tested in combination with the GUI, using a similar variety of input strings and public key values.

def decryption(c):
    """ The decryption function. It takes a list of integers and returns a message in the form of a string."""    
    
    #Local Variables
    v = ''
    w = []
    
    global d
    global n
    
    # Takes each item in list " c " and decrypts it by the following function:  " k = item^d mod(n) ". It then adds it the the decrypted list " w "
    for item in c:
        k = pow(item,d,n)
        w.append(k)
    # Converts list " w " into a string singularly by each item
    for item in w:
        char = chr(item)
        v += char    
    return v

# the decryption() function was tested simultaneously with the encryption() function and under the same conditions.

# ===================================================

#GUI Functions

# ===================================================

# Main GUI Function

def GUIMain():
    """Takes in no inputs, it sets up the GUI elements for this progrma,
    and then runs the event listener loop."""
    
    #global variables
    global rootWin
    global msgBox
    global theirPubInput
    global msgLabel
    
    #Call the find key function to generate key values
    findkeys()
    
    # create the main GUI window
    rootWin = Tk()
    rootWin.title("First example")
    
    # create labels to hold information for the user
    myPubLabel = Label(rootWin, text = "Your Public Key:",
                       font = "Arial 20 bold", fg = "blue",bg='white', relief = GROOVE, justify=CENTER)
    theirPubLabel = Label(rootWin, text = "Their Public Key:",
                          font = "Arial 20 bold", fg = "blue", bg='white', relief = GROOVE, justify=CENTER)
    msgLabel = Label(rootWin, text = "Message Box:",
                              font = "Arial 20 bold", fg = "blue", bg='white', relief = GROOVE, justify=LEFT)    
    myPubDisp = Label(rootWin, text = (e,n),
                              font = "Arial 20 bold", fg = "black", relief = GROOVE, justify=CENTER)    
    
    
    # create entry boxes for (1) inserting a message or encrypted message and (2) the other user's public key.
    theirPubInput = Entry(rootWin, bg = 'white', bd = 5, font = "Times 12", justify = CENTER, relief = GROOVE, width = 20)
    msgBox = Entry(rootWin, bg = 'white', bd = 5, font = "Times 12", justify = LEFT, relief = GROOVE, width = 63)
    
    # create encryption and decryption buttons
    encryptButton = Button(rootWin, text = "Encrypt", font = "Arial 12", bg = "blue", fg = "white", command = encryptButtonResponse)
    decryptButton = Button(rootWin, text = "Decrypt", font = "Arial 12", bg = "blue", fg = "white", command= decryptButtonResponse)
    quitButton = Button(rootWin, text = "Quit",bg = 'white', font = "Arial 16", command = quit)
    
    # place labels inside window
    myPubLabel.grid(row = 0, column = 0, columnspan =3)
    theirPubLabel.grid(row = 0, column = 5, columnspan = 3)
    msgLabel.grid(row = 3, column = 0, columnspan = 4)
    myPubDisp.grid(row=1, column = 0, columnspan = 3)
    
    # place entry boxes inside window
    theirPubInput.grid(row = 1, column = 5, columnspan = 3)
    msgBox.grid(row = 4, column = 0, columnspan = 11, rowspan=3)
    
    # place buttons inside window
    encryptButton.grid(row = 8, column = 6, columnspan = 2)
    decryptButton.grid(row = 8, column = 0)
    quitButton.grid(row = 8, column = 3, columnspan = 2)

    # start the event listener loop going
    rootWin.mainloop()

# The GUIMain() function was developed in increments and tested every step along the way

# =======================================

#Other GUI FUnctions

def quit():
    """This is a callback method attached to the quit button.
    It destroys the main window, which ends the program"""
    rootWin.destroy()
 
# the quit() function was tested simply by pressing the button in the GUI that calls it. The result of this action was as desired.

def outputWindow(k):
    """This is a helper function that is called when the decryption button is pressed. It takes a message as a string and presents it to the user in a pop-up window."""
    outputWin = Toplevel(rootWin)
    outputWin['bg'] = 'white'
    outputWin.title('I am the output window')
    outputMsg = Label(outputWin, text = k,
                                  font = "Arial 20 bold",bg = 'blue', fg = "white", relief = GROOVE, justify=LEFT)        
    outputMsg.grid(row = 0, column = 0, columnspan = 4)
     
# the outputWindow(k) function is a helper function of the function decryptButtonResponse() and was tested in that context along with all the tests that were devised for that.


def encryptButtonResponse():
    """This is a callback method attached to the encrypt button. It takes the inserted public keys (in the form of two integers separated by a space) and the inserted message, calls the theirEncryption function to encrypt the message. It prints an encryption of the message in the form of a string of integers separated by white space."""
    theirKey = theirPubInput.get()
    theirKeys = theirKey.split()
    theirE = theirKeys[0]
    theirN = theirKeys[1]
    msg = msgBox.get()
    theirCList = theirEncryption(msg,theirE,theirN)
    theirCString = "" 
    for i in range(len(theirCList)):
        item = theirCList[i]
        itemString = str(item)
        theirCString = theirCString + itemString + ' '
    print(theirCString)

# the encryptButtonResponse() function is a callback method attached to the encrypt button and was tested by running the program several times, inserting various inputs into the input boxes, and then pressing the encrypt button to see what happens. After some tweaking the functionality was as desired.

def decryptButtonResponse():
    """This is a callback method attached to the decrypt button. It takes the from the message box an encrypted message in the form of a string of integers separated by white space. It calls the decryption function to convert this to a message, which it then presents to the user by calling the helper function outputWindow."""
    InputString = msgBox.get()
    ListWithStrings = InputString.split()
    ListWithIntegers = []
    for i in range(len(ListWithStrings)):
        ListWithIntegers.append(int(ListWithStrings[i]))
    msg = decryption(ListWithIntegers)
    outputWindow(msg)

# the decryptButtonResponse() function is a callback method attached to the decrypt button and was tested by running the program several times, inserting various inputs into the input boxes, and then pressing the decrypt button to see what happens. After some tweaking the functionality was as desired.



# Call the Main GUI function when the program is loaded
GUIMain()
