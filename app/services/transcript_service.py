import re
from app.schemas import TranscriptInput, Line, TranscriptOutput
from typing import List, Tuple
from podcastfy.client import generate_podcast


def clean_tss_markup(input_text: str, additional_tags: List[str] = ["Person1", "Person2"], supported_tags: List[str] = None) -> str:
    """
    Remove unsupported TSS markup tags from the input text while preserving supported SSML tags.

    Args:
        input_text (str): The input text containing TSS markup tags.
        additional_tags (List[str]): Optional list of additional tags to preserve. Defaults to ["Person1", "Person2"].
        supported_tags (List[str]): Optional list of supported tags. If None, use COMMON_SSML_TAGS.
    Returns:
        str: Cleaned text with unsupported TSS markup tags removed.
    """

    if supported_tags is None:
        supported_tags = ['lang', 'p', 'phoneme', 's', 'sub']

    # Append additional tags to the supported tags list
    supported_tags.extend(additional_tags)

    # Create a pattern that matches any tag not in the supported list
    pattern = r'</?(?!(?:' + '|'.join(supported_tags) + r')\b)[^>]+>'

    # Remove unsupported tags
    cleaned_text = re.sub(pattern, '', input_text)

    # Remove any leftover empty lines
    cleaned_text = re.sub(r'\n\s*\n', '\n', cleaned_text)

    # Ensure closing tags for additional tags are preserved
    for tag in additional_tags:
        cleaned_text = re.sub(f'<{tag}>(.*?)(?=<(?:{"|".join(additional_tags)})>|$)',
                              f'<{tag}>\\1</{tag}>',
                              cleaned_text,
                              flags=re.DOTALL)

    return cleaned_text.strip()


def split_qa(input_text: str, ending_message: str = "", supported_tags: List[str] = None) -> List[Tuple[str, str]]:
    """
    Split the input text into question-answer pairs.

    Args:
        input_text (str): The input text containing Person1 and Person2 dialogues.
        ending_message (str): The ending message to add to the end of the input text.

    Returns:
            List[Tuple[str, str]]: A list of tuples containing (Person1, Person2) dialogues.
    """
    input_text = clean_tss_markup(
        input_text, supported_tags=supported_tags)

    # Add placeholder if input_text starts with <Person2>
    if input_text.strip().startswith("<Person2>"):
        input_text = "<Person1> Humm... </Person1>" + input_text

    # Add ending message to the end of input_text
    if input_text.strip().endswith("</Person1>"):
        input_text += f"<Person2>{ending_message}</Person2>"

    # Regular expression pattern to match Person1 and Person2 dialogues
    pattern = r"<Person1>(.*?)</Person1>\s*<Person2>(.*?)</Person2>"

    # Find all matches in the input text
    matches = re.findall(pattern, input_text, re.DOTALL)

    # Process the matches to remove extra whitespace and newlines
    processed_matches = [
        (" ".join(person1.split()).strip(), " ".join(person2.split()).strip())
        for person1, person2 in matches
    ]

    lines = []
    for idx, (person1_text, person2_text) in enumerate(processed_matches):
        lines.append(Line(id=str(2*idx), speaker_id="1", text=person1_text))
        lines.append(
            Line(id=str(2*idx + 1), speaker_id="2", text=person2_text))

    return lines


def generate_transcript(data: TranscriptInput) -> TranscriptOutput:
    # Replace with real NLP/AI logic later
    config = {
        'word_count': 500,
        'conversation_style': ['Fun', 'Playful', 'Curious', 'Educational'],
        'roles_person1': 'Friendly Host',
        'roles_person2': 'Knowledgeable Friend',
        'dialogue_structure': [
            'Warm Welcome',
            'Simple Topic Introduction',
            'Fun Facts & Stories',
            'Interactive Q&A (What do you think?)',
            'Closing with a Song or Rhyme'
        ],
        'podcast_name': 'Little Explorers',
        'podcast_tagline': 'Big ideas for curious kids!',
        'output_language': 'Vietnamese',
        'user_instructions': 'Use simple words, explain with stories and examples children can relate to. Make it cheerful and colorful!',
        'engagement_techniques': [
            'Sound Effects',
            'Songs or Rhymes',
            'Questions to the Listener',
            'Short Stories',
            'Funny Comparisons',
            'Animal Sounds or Voices'
        ],
        'creativity': 0.2,
    }

    transcripts_raw = generate_podcast(
        urls=data.source_urls,
        image_paths=data.image_urls,
        text=data.text,
        conversation_config=config,
        transcript_only=True,
        llm_model_name="gemini-2.0-flash-001",
    )
    with open(transcripts_raw, 'r', encoding='utf-8') as file:
        transcript_content = file.read()

    return TranscriptOutput(transcript=split_qa(transcript_content))
