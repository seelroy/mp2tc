import re
import asyncio
import logging
import aiohttp
import base64
import pyxivapi
from tqdm import tqdm
from pyxivapi.models import Filter, Sort

async def fetch_item_ids(item_names, progress_bar, description):
    # Get your API key at xivapi.com
    client = pyxivapi.XIVAPIClient(api_key="key")

    item_ids = {}

    for item_name in progress_bar(item_names, desc=description):
        try:

            recipe = await client.index_search(
            name=item_name, 
            indexes=["Item"], 
            columns=["ID"]
        )

            if recipe and "Results" in recipe and len(recipe["Results"]) > 0:
                item_id = recipe["Results"][0]["ID"]
                item_ids[item_name] = item_id
            else:
                logging.warning(f"Item '{item_name}' not found.")

        except Exception as e:
            logging.error(f"Error fetching ID for item '{item_name}': {e}")

    await client.session.close()
    return item_ids



async def parse_text_file(list_filename):
    furniture_names = []
    furniture_quantity = []
    dye_names = []
    dye_quantity = []
    current_section = None

    with open(list_filename, 'r') as file:
        for line in file:
            line = line.strip()

            if line == "Furniture":
                current_section = "Furniture"
                continue
            elif line == "Dyes":
                current_section = "Dyes"
                continue
            elif line == "Furniture (With Dye)":
                current_section = None
                continue

            if current_section and line:
                # Use regex to extract item names and numbers
                match = re.match(r'^(.*?):\s*(\d+)$', line)
                if match:
                    item_name = match.group(1)
                    item_number = int(match.group(2))

                    if current_section == "Furniture":
                        furniture_names.append(item_name)
                        furniture_quantity.append(item_number)
                    elif current_section == "Dyes":
                        dye_name = f"{item_name} Dye"
                        dye_names.append(dye_name)
                        dye_quantity.append(item_number)

    return furniture_names, furniture_quantity, dye_names, dye_quantity

async def main(list_filename):
    # Split names and quantity
    furniture_names, furniture_quantity, dye_names, dye_quantity = await parse_text_file(list_filename)

    # Fetch item IDs
    furniture_description = "Fetching IDs for Furniture"
    dye_description = "Fetching IDs for Dyes"
    furniture_ids = await fetch_item_ids(furniture_names, tqdm, furniture_description)
    dye_ids = await fetch_item_ids(dye_names, tqdm, dye_description)

    items_list = []
    for item_name, item_quantity in zip(furniture_names + dye_names, furniture_quantity + dye_quantity):
        item_id = furniture_ids.get(item_name) or dye_ids.get(item_name)
        if item_id is not None:
            items_list.append(f"{item_id},null,{item_quantity}")

    # Convert the list to a string with ; as the separator
    items_string = ";".join(items_list)

    #Encode in base64 for Teamcraft
    base64_encoded_items = base64.b64encode(items_string.encode()).decode()
    teamcraft_url = f"https://ffxivteamcraft.com/import/{base64_encoded_items}"

    # Print the URL
    print("Teamcraft URL:")
    print(teamcraft_url)

    # Save the URL
    with open("teamcraft_url.txt", "w") as url_file:
        url_file.write(teamcraft_url)



if __name__ == '__main__':
    # Basic log for each API request
    #logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')

    print("mp2tc - https://github.com/seelroy/mp2tc")
    
    # Request the file name from user
    list_filename = input("Enter the filename of the furniture list: ")

    # Add extension if not added
    if not list_filename.endswith(".txt"):
        list_filename += ".txt"


    asyncio.run(main(list_filename))