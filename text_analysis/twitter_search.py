from TwitterSearch import *
import time
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['Логан', 'Росомаха']) # let's define all words we would like to have a look for
    tso.set_language('ru') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'MZXh5bXLtg7qlVFdEIdlU7HIN',
        consumer_secret = 'JcyDytkE53O76SsRJgcqYQmxEZ1GGGNvF9NajyqNxECtoBriFA',
        access_token = '842681523010781184-PGOHtuhmPYWJOCs9qaEItALoxjybOC2',
        access_token_secret = 'fQACVaLpKm5JlV6rzi0rBR4mYMejXCDJxofoigiyaKAXQ'
     )

     # this is where the fun actually starts :)
    def my_callback_closure(current_ts_instance):  # accepts ONE argument: an instance of TwitterSearch
        queries, tweets_seen = current_ts_instance.get_statistics()
        if queries > 0 and (queries % 5) == 0:  # trigger delay every 5th query
            time.sleep(60)  # sleep for 60 seconds

    for tweet in ts.search_tweets_iterable(tso):
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)