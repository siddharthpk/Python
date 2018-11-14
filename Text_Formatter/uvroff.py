import sys
import fileinput

# Global 
# Using dictonaries to initialise default value/state
var = { '.FT': False,'.LW': 0,'.LM': 0,'.LS': 0}

state = {'line_length': 0, 'is_different': False}

def main ():

    """
    Format according to given control sequences.
    """

    # Define our variables.
    # The currently calculated output.

    out = ""

    # Process each line. If we detect a control sequence on the line, return none. If we detect [], add an extra newline. Otherwise just   	 check for paragraph size and margin. The output will be joined with 'out'

    lines =  [ line for line in fileinput.input() ]
    processed = [ process_line(line) for line in lines]
    not_empty = [ line for line in processed if line != None ]
    
    if len(not_empty) == 0:
        return
    else:
        out = "".join(not_empty)
        print out
    
def process_line (line):

    global var, state

    """ 
    Process the line. Check for control sequences, set any flags required. Format appropriately.
    """  

    split = line.split()

    # Detect control sequences.
    if len(split) is not 0:
        if split[0] == ".FT":
            if split[1] == "off":
                var['.FT'] = False
            elif split[1] == "on":
                var['.FT'] = True
            return None

        elif split[0] == ".LW": # Also turns on .FT
            if isinstance(int(split[1]), int):
                var['.LW'] = int(split[1])
                var['.FT'] = True
            elif split[1][0] == '-':
                var['.LW'] -= int(split[1][1:])
                var['.FT'] = True
            elif split[1][0] == '+':
                var['.LW'] += int(split[1][1:])
                var['.FT'] = True
            return None

        elif split[0] == ".LM":
            if split[1][:1] == "-":
                var['.LM'] -= int(split[1][1:])
                if var['.LM'] < 0:
                    var['.LM'] = 0
            elif split[1][:1] == "+":
                var['.LM'] += int(split[1][1:])
            else:
                var['.LM'] = int(split[1])

            # Restriction on margins.
            if var['.LM'] > var['.LW'] - 20:
                var['.LM'] = var['.LW'] - 20
            return None
            
    # output the line
    
    if var['.FT']:
     
        # Special case for empty lines.
        if split == []:
            state['line_length'] = 0
            if state['is_different']:
                return '\n'
            else:
                state['is_different'] = True
                return '\n\n'
        state['is_different'] = False
        
        # Do we need a margin? (Is this a new line?)
        if state['line_length'] == 0:
            out = "".join( [" " for i in range(var['.LM']) ] )
            state['line_length'] = var['.LM']
        else:
            out = ""
            
        # Gradually add each word, making sure we're not going over the .LW
        for word in split:
          
	    # Do we need a new line?
            if state['line_length'] + len(word) >= var['.LW']:
                margin = "".join( [" " for i in range(var['.LM']) ] )
                out = out + '\n' + margin
                state['line_length'] = var['.LM']
            # Otherwise, add a space
            elif state['line_length'] != var['.LM']:
                state['line_length'] += 1
                out = out + ' '
            # Concatenate
            out = out + word
            state['line_length'] += len(word)
        
	return out
    else:
        return line
    

if __name__ == "__main__":
    main()
