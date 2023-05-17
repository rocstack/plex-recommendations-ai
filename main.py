import logging
import openai
from plexapi.server import PlexServer
from utils.classes import UserInputs

userInputs = UserInputs(
    plex_url="<server>",
    plex_token="<plex token>",
    openai_key="<open-ai key>",
    library_name="<Library name>",
    collection_title="Recommended For You",
    history_amount=100,
    recommended_amount=30,
    minimum_amount=5
)

openai.api_key = userInputs.openai_key

def create_collection(plex, movie_items, description, library):
    movie_list = []
    for item in movie_items:
        movie_search = plex.search(item, mediatype="movie", limit=3)
        if len(movie_search) > 0:
            movie_list.append(movie_search[0])
            logging.info(item + " - added")
        else:
            logging.info(item + " - not found")

    if len(movie_list) > userInputs.minimum_amount:
        try:
            collection = library.collection(userInputs.collection_title)
            collection.removeItems(collection.items())
            collection.addItems(movie_list)
            collection.editSummary(description)
            logging.info("Updated pre-existing collection")
        except:
            collection = plex.createCollection(
                title=userInputs.collection_title,
                section=userInputs.library_name,
                items=movie_list
            )
            collection.editSummary(description)
            logging.info("Added new collection")
    else:
        logging.info("Not enough movies were found")

def run():
    # Connect
    try:
        plex = PlexServer(userInputs.plex_url, userInputs.plex_token)
        logging.info("Connected to Plex server")
    except Exception as e:
        logging.error("Plex Authorization error")
        return

    try:
        # Find history items for the library
        library = plex.library.section(userInputs.library_name)
        account_id = plex.systemAccounts()[1].accountID

        # a = library.hubs()

        items_string = ""
        history_items_titles = []
        watch_history_items = plex.history(librarySectionID=library.key, maxresults=userInputs.history_amount, accountID=account_id)
        logging.info("Fetched items")

        for history_item in watch_history_items:
            history_items_titles.append(history_item.title)

        items_string = ", ".join(history_items_titles)
        logging.info("Found " + items_string + " to base recommendations off")

    except Exception as e:
        logging.error("Failed to get watched items")
        return

    try:
        query = "Can you give me movie recommendations based on what I've watched? "
        query += "I've watched " + items_string + ". "
        query += "Can you base your recommendations solely on what I've watched already. "
        query += "I need around " + str(userInputs.recommended_amount) + ". "
        query += "Please give me the comma separated result, and then a short explanation separated from the movie values, separated by 3 pluses like '+++'."
        query += "Not a numbered list. "

        # create a chat completion
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
        ai_result = chat_completion.choices[0].message.content
        ai_result_split = ai_result.split("+++")
        ai_movie_recommendations = ai_result_split[0]
        ai_movie_description = ai_result_split[1]

        movie_items = ai_movie_recommendations.split(",")
    except:
        logging.error('Was unable to query openai')
        return

    if len(movie_items) > 0:
        create_collection(plex, movie_items, ai_movie_description, library)

if __name__ == '__main__':
    run()