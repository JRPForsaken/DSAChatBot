import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load data from {file_path}. Initializing with an empty knowledge base.")
        data = {"questions": []}
        save_knowledge_base(file_path, data)

    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def load_responses(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load responses from {file_path}.")
        return {"responses": {}}

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def chat_bot(responses_data: dict, knowledge_base_file: str):
    print("Hello, welcome to the customer support section. The following is a list of options for any queries you may have when purchasing/availing our services:")
    print("1. Payment\n2. Delivery\n3. Seasonal availability\n4. Contact information\n5. Other FAQ\n6. Feedback")
    print("———————————————————————————")

    try:
        knowledge_base: dict = load_knowledge_base(knowledge_base_file)
    except FileNotFoundError:
        print(f"Error: Could not find {knowledge_base_file}. Make sure the file exists.")
        return

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == 'quit':
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        elif user_input.lower() == '1':
            # Payment Section
            payment_responses = responses_data["responses"]["payment"]
            print(payment_responses["intro"])
            print("\nThe available payment options are:")
            for option in payment_responses["options"]:
                print(f"* {option}")
            print(payment_responses["issue_responses"][1])

        elif user_input.lower() == '2':
            # Delivery Section
            delivery_responses = responses_data["responses"]["delivery"]
            print(delivery_responses["intro"])
            
            
        elif user_input.lower() == '3':
            # Seasonal Availability Section
            seasonal_responses = responses_data["responses"]["seasonal_availability"]
            print(seasonal_responses["intro"])
            
            social_media_links = seasonal_responses["social_media"]
            print(f"Facebook: {social_media_links['facebook']}")
            print(f"Twitter: {social_media_links['twitter']}")
            print(f"Instagram: {social_media_links['instagram']}")

        elif user_input.lower() == '4':
            # Contact Information Section
            contact_responses = responses_data["responses"]["contact_information"]
            print(contact_responses["intro"])
            print(f"Business Telephone: {contact_responses['telephone_numbers']['business']}")
            print(f"Phone Number Alternative: {contact_responses['telephone_numbers']['alternative']}")
            print(f"You may reach us at our customer service social media page where our staff can assist you better. You can head over there using this link: {contact_responses['social_media_link']} or search us on our social media handles @(BusinessName).")

        elif user_input.lower() == '5':
            # Other FAQ Section
            faq_responses = responses_data["responses"]["other_faq"]
            print(faq_responses["intro"])
            print(f"If you have any concerns that’s not listed in the FAQ, you can check out our FAQ section on our website through this link: {faq_responses['faq_link']}")
            print("You can also reach out to our contact information for assistance.")

        elif user_input.lower() == '6':
            # Feedback Section
            feedback_responses = responses_data["responses"]["feedback"]
            print("How would you rate our services on a scale of 1-10?")
            rating = int(input("Your rating: "))
            if rating <= 4:
                print(feedback_responses["intro_low_rating"])
                user_feedback = input("*User will type message*\n")
                print(feedback_responses["user_response"])
            elif rating >= 5:
                print(feedback_responses["intro_high_rating"])
                user_feedback = input("*User will type message*\n")
                print(feedback_responses["user_response"])
            else:
                print("Invalid rating. Please provide a rating between 1 and 10.")

        else:
            print(f'Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base(knowledge_base_file, knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    # Load responses from the JSON file
    responses_file = 'responses.json'
    responses_data = load_responses(responses_file)

    # Pass the knowledge base file path to the chat_bot function
    chat_bot(responses_data, 'knowledge_base.json')
