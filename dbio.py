import asyncio
import aiopg

import sys
import os

import random
import time


alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def IDGenerator():
    n = int(time.time())
    
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(alphabet[int(n % len(alphabet))])
        n //= len(alphabet)

    return "".join(digits[::-1] + random.sample(alphabet, k=2))
    


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



class Database():
    @classmethod
    async def connect(cls):
        """
        Connects to the database with an optional current connection.\n
        This is so that the class can cache data for the bot.
        """
        self = Database()

        self.con = None
        while not self.con:
            try:
                self.con = await aiopg.create_pool (
                    user =      os.getenv("DB_USER"),
                    password =  os.getenv("DB_PASSWORD"),
                    host =      os.getenv("DB_HOST"),
                    port =      "5432",
                    dbname =    os.getenv("DB_NAME"),
                    pool_recycle = 100,
                    maxsize  =  10
                )
            except:
                await asyncio.sleep(1)

        return self




    ###########################################
    ########### Manage Redirects ##############
    ###########################################


    async def add_redirect(self, redirect: str):
        """
        Adds a redirect to the database\n
        Will return the ID (string) that it has been assigned
        """

        uri = IDGenerator()

        with (await self.con.cursor()) as cur:
            await cur.execute(
                "INSERT INTO links (uri, redirect) VALUES (%s, %s)", 
                (uri, redirect)
            )

        return uri



    async def get_redirect(self, uri: str):
        """
        Gets the redirect link for a uri ID
        """

        with (await self.con.cursor()) as cur:
            await cur.execute("SELECT redirect FROM links WHERE uri = %s", (uri, ))
            response = await cur.fetchone()

        return response[0] if response else None



    async def del_redirect(self, uri: str):
        """
        Deletes a redirect from the database
        """

        with (await self.con.cursor()) as cur:
            await cur.execute("DELETE FROM links WHERE uri = %s", (uri, ))