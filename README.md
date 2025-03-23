**What is this?**

This is a kind of "game about software development".
Your goal is to write the "intelligence" piece of a Negamax algorithm (see https://en.wikipedia.org/wiki/Negamax) and defeat our Resident AI in a connect 4 match (see https://en.wikipedia.org/wiki/Connect_Four)

Basically you'll have to write a **scoring function** that returns the amount of points that sums a given board, under the current player point of view. Amount of points indicates how favourable current situation is.
Theory says that the more accurate your estimation is, more probability of victory you'll have.

A Board class with some helper method is provided for counting lines of coins and other stuff, check it out.

**Currently we are still in early access, so you will find bugs, and all discussed here may change** 
in any time :-)

**Installation**

pip install -r requirements.txt

**Usage**

scoring_function module is where estimation function is located, improve it as much as you can!

Execute run.sh to test it against Resident AI. Currently it is deployed on a free cloud service, be patient :-)

A client is provided here             
https://connect4-api.onrender.com/client

API documentation, if you want to write your own client. PRs are welcome too :-)  
https://connect4-api.onrender.com/docs

**Known bugs**

Sometimes SSE client used yields invalid JSON responses, it seems to be related to the following issue    
https://github.com/btubbs/sseclient/issues/28

