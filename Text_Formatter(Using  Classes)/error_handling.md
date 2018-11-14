The possible errors that I could think of that can occur are the following:
1. Invalid Filename
2. Invalid File extension
3. Invalid Format Commands:
    3a. Format State is neither "on" nor "off"
    3b. No numerical value provided for either of LW, LM & LS
 
1. Invalid Filename: Raises the error when the name doesn't consist of characters between the
ASCII values. Tells the user to provide correct filename.

2. Invalid File Extension: Raises the error if the file isn't a .txt file. Checks using "." as a split delimiter.If the next token isnt "txt", it sends the error.

3. Invalid Format Commands: Error raised whenever ecountered.
	3a. If the 'FT' state is neither on nor off, 'FT' assigned "off"
	3b. If numerical value isn't provided for any of the other format cmds, 0 is assigned. 
