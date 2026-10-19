Select such that you can lısten for the knowledgebase(bug reports, issues, commits etc) 
How can you use this knowledgebase to improve sw quality and code agents checking for code quality, comparing previous metrics with current ones(like deploy times, test running  times)

What can you offer to developers using this kind of a system?

Find some git repos to test the system you will build?

Use genAI while building the system, use it as a partner, use Claude code

Use Claude code to develop a framework to replay everything in a repo for the testing side of the system we will build, think of it like this when you build the system and it will give some insights from the past data and we will replay to understand if system is giving proper insights

1- decide on knowledgebase inputs and outputs

15 ekim

Timemachine yap, her infoyu timestampleyerek

We just give an llm knowledge base and the the repo with replaying(only using info up to that date)

Here are my general notes from the sessions with the professor use the info in them but here i will explain what i understand from the project, first there will be an agentic system of a knowledgebase, LLMS from claude code will benefit from this knowledge base of the repo, you can check the PROJECT.pdf in this directory to see how do we plan to build the knowledge base what should we have in it what are the outputs we want to have etc and also we will have a time machine, as a second system which will let us test the first system we have. this time machine will only let the first system see up to the specific time frame we give and first system will try to get insights from that time frame, and by this second system(time machine) we will be able to test the success of our actual system(we have the success and test criteria in the PROJECT.pdf)