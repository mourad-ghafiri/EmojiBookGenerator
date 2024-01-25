import os
from emoji_story_generator import generate_emoji_story
import json
from jinja2 import Environment, FileSystemLoader
import pdfkit

# "Love, Adventure, Magic, Fun, Memes, Secret, Motivation, Dream, Joke"
subjects = "comedy"
included_topics = ''
excluded_topics = 'religion, politics, violence'
audience = "children"
nbr_emojis = 5
stories = "["

i = 1
n = 160
while i < n:
    try:
        print(f"Generating Story {i} :")
        story = generate_emoji_story(subjects, included_topics, excluded_topics, audience, nbr_emojis)
        print(story)
        stories = stories + story
    except:
        print(f"Story {i} : error\n")
    else:
        print(f"Story {i} : success\n")
        i += 1
    if i < n:
        stories = stories + ",\n"

stories = stories + "\n]"

json_file = open("emojis_stories_for_children_volume_3.json", "w")
n = json_file.write(stories)
json_file.close()


book_asset_path = "books/emojis_stories_for_children_volume_3"
# Load the JSON file
with open(json_file, 'r') as file:
    data = json.load(file)

# Create a list to hold pages
pages = []

# Iterate through the stories, creating pages with 3 stories each
for i in range(0, len(data), 3):
    stories = data[i:i+3]
    page = {"page": i // 3, "stories": stories}
    pages.append(page)

# Save the new JSON to a file
with open(f'{book_asset_path}/book_pages.json', 'w') as file:
    json.dump(pages, file, indent=2)

environment = Environment(loader=FileSystemLoader("books/template/"))
template = environment.get_template("book_template.html")

results_filename = f"{book_asset_path}/book.html"

context = {
    "pages": pages,
}
with open(results_filename, mode="w", encoding="utf-8") as results:
    results.write(template.render(context))
    print(f"... wrote {results_filename}")
