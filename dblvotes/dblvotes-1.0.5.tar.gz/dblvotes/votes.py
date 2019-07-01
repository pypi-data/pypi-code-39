import aiohttp, asyncio,json
#from . import client as ClientToken

async def vote_updates(client,timer=60,):
         """
            client = your DBL token
            timer = delay between checks. Defaults to 60 seconds.

            If user has voted, it will return True.
            If the user HAS NOT voted, it will return False.
            Keep that in mind!
         """
         loop = asyncio.get_event_loop()
         def _getVoteUpdate():
            try:
             PreviousText=open("votes_temp.txt", "r+")
             PreviousText = PreviousText.read()
                 
            except FileNotFoundError:
                PreviousText=open ("votes_temp.txt", "w+") 
                voteurl="https://discordbots.org/api/bots/543966796944769044/votes"
                async with aiohttp.ClientSession(headers=client).get(voteurl) as r:
                    text=r.text()
                PreviousText.write(text)
                        
            voteurl="https://discordbots.org/api/bots/543966796944769044/votes"
            async with aiohttp.ClientSession(headers=client).get(voteurl) as r:
                    text=r.text()
                
                
             

            if PreviousText != text:
                print("User Voted")
                return True
                with open("votes_temp.txt", 'w') as CurrentText:
                    CurrentText.write(text)
         loop.run_forever(getVoteUpdate)
        
