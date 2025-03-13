import subprocess
from character import create_character
from gamestate import game_state

# Create a new character
def main():
    instructions_setting = load_model_instructions('model_instructions_setting.txt')
    instructions_actions = load_model_instructions('model_instructions_actions.txt')
    character = create_character()
    
    gameloop(instructions_setting, instructions_actions)

def load_model_instructions(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
def gameloop(instructions_setting, instructions_actions):

    while True:  
        setting = generate_setting(instructions_setting)
        actions = generate_actions(instructions_actions, setting)
        
        print(f"Setting: {setting.stdout.strip()}\n")
        print(f"{actions[0].stdout.strip()}\n")
        print(f"{actions[1].stdout.strip}\n")
        print(f"{actions[2].stdout.strip}\n\n")

        choice = input("Which option do you choose? 1., 2., or 3.? \n")
        action = actions[int(choice)-1]
        game_state["chosen_action"].append(action)
        game_state["setting/action"].append({setting: action})
        
        print(f"\nYou chose: {action.stdout.strip()}\n")
    
def generate_setting(instructions_setting):
    previous_setting = game_state["setting/action"][-3:] if len(game_state["setting/action"]) > 3 else game_state["setting/action"]
    prompt = f"Generate a new setting.\n\nPrevious setting/action: {previous_setting}\n\n{instructions_setting}"
    setting = subprocess.run(['ollama', 'run', 'mistral', prompt], capture_output=True, text=True)
    print("Generating setting: done\n")
    return setting

def generate_actions(instructions_actions, setting):
    prompt_action_1 = f"Generate action (1.) bbased on the current setting: {setting}\n\n{instructions_actions}"
    action_1 = subprocess.run(['ollama', 'run', 'mistral', prompt_action_1], capture_output=True, text=True)
    game_state["actions"][0] = action_1
    print("Generating action 1: done\n")
    
    prompt_action_2 = f"Generate action (2.) based on the current setting: {setting}\n\n{instructions_actions}"
    action_2 = subprocess.run(['ollama', 'run', 'mistral', prompt_action_2], capture_output=True, text=True)
    game_state["actions"][1] = action_2
    print("Generating action 2: done\n")
    
    # prompt_action_3 = f"Generate action (3.) bbased on the current setting: {setting}\n\n{instructions_actions}"
    # action_3 = subprocess.run(['ollama', 'run', 'mistral', prompt_action_3], capture_output=True, text=True)
    # game_state["actions"][2] = action_3
    # print("Generating action 3: done\n")
    action_3 = None
    
    return [action_1, action_2, action_3]



if __name__ == "__main__":
    main()

