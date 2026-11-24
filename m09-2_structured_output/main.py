from google import genai
from typing import Literal
from pydantic import BaseModel, Field, ValidationError
import os
from dotenv import load_dotenv
import sys

load_dotenv()

class StoryboardError(Exception):
    pass

class Shot(BaseModel):
    scene: str = Field(description="Describe what is in the scene")
    camera_move: Literal["static", "dolly_in", "orbit", "crane_up", "handheld"]
    duration_sec: int = Field(description="Duration of the scene in seconds")
    prompt: str = Field(description="Prompt for the scene")

class Storyboard(BaseModel):
    title: str = Field(description="Name of the video")
    shots: list[Shot]

SYSTEM_PROMPT = """
You are a storyboard artist for an AI video generation service.
The user gives a short brief for a video. Turn it into a storyboard: a title and a list of shots.

Rules for the storyboard:
- 2 to 6 shots.
- The sum of duration_sec of all shots must be 30 or less.
- If the brief asks for a longer video, compress it into 30 seconds and keep the most important moments.
- If the brief gives a duration of 30 seconds or less, match it as closely as possible.
- Each shot is 2 to 10 seconds long, whole seconds only.
- Shots must follow a logical order: establish the place first, then move to details or action.

camera_move must be exactly one of these values:
- static: the camera does not move
- dolly_in: the camera moves slowly toward the subject
- orbit: the camera circles around the subject
- crane_up: the camera rises up and reveals the scene
- handheld: a slightly shaky, documentary-style camera

For each shot:
- scene: one short sentence describing what is on screen.
- prompt: a detailed prompt for a video generation model, in English.
  Describe the subject, the setting, the lighting, the mood and the visual style.
  Do not mention camera movement in the prompt; it is set by camera_move.
  Do not ask for text, logos or subtitles on screen.

Write the title, scene and prompt in English, even if the brief is in another language.
"""

def make_storyboard(brief: str) -> Storyboard:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prev_id = None
    for _ in range(2):
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=brief,
            system_instruction=SYSTEM_PROMPT,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": Storyboard.model_json_schema()
            },
            previous_interaction_id=prev_id
        )
        try:
            output = Storyboard.model_validate_json(interaction.output_text)
        except ValidationError as e:
            prev_id = interaction.id
            brief = f"{e}"
            sys.stderr.write(f"Ошибка при валидации ответа:{e}\n")
            continue

        err = False
        brief = ""

        if len(output.shots) > 6 or len(output.shots) < 2:
            err = True
            prev_id = interaction.id
            brief += f"Total count of scenes is {len(output.shots)}. It must be between 2 and 6 scenes. Fix it\n"
            sys.stderr.write("Неверное количество сцен\n")

        duration = 0
        for shot in output.shots:
            if shot.duration_sec > 10 or shot.duration_sec < 2:
                err = True
                prev_id = interaction.id
                brief += f"Duration of {shot.scene} scene is {shot.duration_sec}. It must be between 2 and 10 seconds. Fix it\n"
                sys.stderr.write("Неверная длительность сцены\n")
            duration += shot.duration_sec

        if duration > 30:
            err = True
            prev_id = interaction.id
            brief += f"Total duration of scenes is {duration}. It must be 30 seconds or less. Decrease scenes\n"
            sys.stderr.write("Общая длительность больше 30 секунд\n")

        if err:
            continue

        return output
    raise StoryboardError(brief)
    
print(make_storyboard("Streets of Astana at night"))