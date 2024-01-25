import openai

openai.organization = ""
openai.api_key = ""


def get_top_writers(subjects):
    prompt = f'''
    give me the list of 3 writers randomly from top 100 of the greatest {subjects} writers in history.
    give me only the names, don't add any other text.
    give me the output in a comma separated line
    '''
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role": "user", "content": prompt
    }])
    return completion.choices[0].message.content


def generate_emoji_story(subjects, included_topics, excluded_topics, audience, nbr_emojis):
    try:
        top_writers = get_top_writers(subjects)
        role = f"Act as {top_writers} combined in one writer using emojis to write for {audience} audience"
        instruction_included_topics = ""
        instruction_excluded_topics = ""
        if included_topics:
            instruction_included_topics = f"I want you to include the following topics: {included_topics} in your writing"
        if excluded_topics:
            instruction_excluded_topics = f"I want you to exclude the following topics: {excluded_topics} from your writing"
        question = f'''
        Give me the output only as json with this structure, without any explanation or additional text:
         - emoji_story: the short emoji story.
         - story: the translation of the story, insert emojis.
         - title: a creative title of the story in english without emojis.
         - subjects: {subjects}
         - audience: {audience}
         - tags: array of tags of the story
         - nbr_emojis: {nbr_emojis}
        '''

        prompt = f'''
        {role}.
        I want you to write a creative short story with exactly {nbr_emojis} emojis.
        {instruction_included_topics}.
        {instruction_excluded_topics}.
        I want you to provide a short translation like this example in the structure only:
        "emoji_story": "📝👩‍💼💌💔👨‍💼",
        "story": "Once upon a time, a busy 📝 working woman 👩‍💼 received a love letter 💌 from her colleague 👨‍💼. But their love was not meant to be 💔.".
    
        {question}
        '''
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
            "role": "user", "content": prompt
        }])
        return completion.choices[0].message.content
    except:
        return "error while generating the story"
