from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from character import create_character
from gamestate import game_state

# Initialize the OpenAI model with a valid model name
llm = ChatOpenAI(model="gpt-4o-mini")  # or "gpt-4"

def main():
    instructions_setting = load_model_instructions('model_instructions_setting.txt')
    instructions_actions = load_model_instructions('model_instructions_actions.txt')
    character = create_character()
    game_state["character"] = character

    gameloop(instructions_setting, instructions_actions)

def load_model_instructions(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
def gameloop(instructions_setting, instructions_actions):

    while True:  
        setting = generate_setting(instructions_setting)
        generate_actions(instructions_actions, actions=3)
        
        print(f"{setting}\n")
        print(f"{game_state["current_actions"][0]}")
        print(f"{game_state["current_actions"][1]}")
        print(f"{game_state["current_actions"][2]}\n")

        choice = input("Which option do you choose? 1/2/3 or a custom action? ")
        if choice.isdigit():
            action = game_state["current_actions"][int(choice)-1]
        else:
            action = choice
        game_state["history"].append({setting: action})
        if len(game_state["history"]) > 6:
            game_state["history"].pop(0)

        # print(f"\n------\nGame_state:\n{game_state}\n------\n")
        
        print(f"\nYou chose: {action}\n")
    
def generate_setting(instructions_setting):
    previous_setting = None
    previous_action = None

    if game_state["history"]:
        last_entry = game_state["history"][-1]
        previous_setting = list(last_entry.keys())[0]
        previous_action = last_entry[previous_setting][-1]  # Get the last action taken
    
    # print(f"Previous setting: {previous_setting_key}")
    # print(f"Previous action: {previous_action}")
    
    prompt = f"""Generate a new setting based on:
    Previous setting: {previous_setting} 
    Previous action: {previous_action}
    Game state: {game_state}
    {instructions_setting}"""

    setting = llm.invoke(prompt)
    new_setting = setting.content

    game_state["current_setting"] = new_setting
    game_state["current_actions"] = []

    return new_setting

def generate_actions(instructions_actions, actions):
    game_state["current_actions"] = []
    for action_no in range(1, actions+1):

        prompt = f"""Start with '{action_no}'. Then generate one action based on: 
        Current setting: {game_state["current_setting"]} 
        Game state: {game_state}
        Previous actions in this setting: {game_state["current_actions"]}
        {instructions_actions}"""

        action = llm.invoke(prompt)
        game_state["current_actions"].append(action.content)

if __name__ == "__main__":
    main()

