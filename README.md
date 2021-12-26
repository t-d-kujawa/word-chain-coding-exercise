# Word Chain Coding Exercise
When running *WordChain.py*, the program will ask for the first and last words, then print a chain starting with the first word and ending with the last word. The chain will have the minimum possible length, but there may be other possible chains with the same length.

Additional options are available by adding the following flags when running *WordChain.py*:

- -d or --dictionary will allow you to choose a different dictionary for that chain
- -l or --length will allow you to remove "add a character" and "remove a character" as possible chain steps, forcing all steps in the chain to be the same length
- -q or --quiet will reduce the output to simply list the steps in the chain, with a blank list for no possible chain
- -w or --words will allow you to specify the first and last words in advance and skip the prompt
- -h or --help will list these options