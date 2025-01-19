from typing import Tuple
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI


def find_song_from_lyrics(lyrics: str) -> Tuple[str, str]:
    """
    Given song lyrics, attempts to determine the song title and the singer.

    Args:
        lyrics (str): The lyrics of the song.

    Returns:
        Tuple[str, str]: The song title and singer's name.
    """
    summary_template = """
    Given the following song lyrics:
    {lyrics}
    Please determine:
    - The song title
    - The artist or singer

    Format your response as:
    Song Title: <title>
    Artist: <artist>
    """

    prompt = PromptTemplate(
        input_variables=["lyrics"],
        template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    formatted_prompt = prompt.format(lyrics=lyrics)

    response = llm.invoke(input=formatted_prompt)

    print(f"Response Object: {response}")

    try:
        response_text = response['text'] if isinstance(response, dict) else response.content.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from the response object: {e}") from e

    try:
        lines = response_text.split("\n")
        title_line = next(line for line in lines if line.startswith("Song Title:"))
        artist_line = next(line for line in lines if line.startswith("Artist:"))

        title = title_line.replace("Song Title:", "").strip()
        artist = artist_line.replace("Artist:", "").strip()
        return title, artist
    except Exception as e:
        raise ValueError(f"Unexpected response format: {response_text}") from e


if __name__ == "__main__":
    load_dotenv()

    print("Enter song lyrics:")
    user_lyrics = input("Lyrics: ")

    try:
        song_title, artist = find_song_from_lyrics(user_lyrics)
        print(f"\nIdentified Song:\nTitle: {song_title}\nArtist: {artist}")
    except Exception as e:
        print(f"Error: {e}")
