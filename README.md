# monday
This repo is used to extract data from [Monday.com's GraphQL API](https://api.developer.monday.com/docs) into this a Googlesheet

- The [monday_boards.py](/monday_boards.py/) script extracts data from the individual boards listed in the Googlesheet mentioned above, the list can be updated by anyone at, when a board is added the script extracts the data from Monday.com into a corresponding tab in the Googlesheet. 

To add a new board, fill the info in the Googlesheet  then create a new tab with the same name as in column B, finally share the board on Monday.com with ```help@google.com```.

Next time the process executes it will automatically extract the data into the new tab you created.

The ID column refers to the number in the URL string of the monday board.

The script is executed every 30mins

