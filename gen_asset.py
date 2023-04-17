import openai
openai.api_key = "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"


# Generate assets from OpenAI API
def generate_game_asset(prompt):
    naruto_prompt = f"{prompt}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=naruto_prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return response.choices[0].text.strip()