import config,step5

"""
Step 5 continued.
User interface to determine evalue cutoff for mature.py. Run after step 5.
"""

def question():
    invalid_input = True
    ecutoff = config.C['mature_evalue_cutoff']
    while invalid_input:
        question1 = raw_input('Would you like to continue with the output from step 5 with an ecutoff \
value of {}? Please type y for yes or n for no: '.format(ecutoff))
        
        if question1 == 'y':
            print "You said yes. Let's keep going!\n"
            invalid_input = False
            return 
            
        elif question1 == 'n':
            print 'You said no.'
            question2 = raw_input('Would you like to repeat step 5 with a new evalue cutoff?\
 Please type y for yes or n for no: ')
            
            if question2 == 'y':
                ecutoff = raw_input('You said yes. Please type in the ecutoff value you would like to use: ')
                print 'The new mature ecutoff is {}'.format(ecutoff)
                step5.run(float(ecutoff))
                continue
            
            elif question2 == 'n':
                print 'You said no. Goodbye!'
                exit()
            
        else:
            print 'Sorry, that was an invalid input!'
