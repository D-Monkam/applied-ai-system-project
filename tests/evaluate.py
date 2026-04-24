import os
import sys
from dotenv import load_dotenv

# This adds the parent directory to the Python path
# so it can find the pawpal_system and pet_care_advisor modules.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pawpal_system import Owner, Pet
from pet_care_advisor import PetCareAdvisor

# Load environment variables (for the Google API key)
load_dotenv()

def evaluate_advisor():
    """
    Runs a suite of tests against the PetCareAdvisor to evaluate its performance
    using a keyword-based threshold scoring system.
    """
    print("--- Starting PetCareAdvisor Evaluation ---")

    # --- Define Test Cases ---
    # Each test case now includes a 'pass_threshold' (0.0 to 1.0).
    test_cases = [
        {
            "name": "Dog - Anxiety Advice",
            "question": "My dog gets really scared during thunderstorms. What can I do to help him?",
            "pet_context": {"name": "Max", "breed": "Beagle", "age": 4, "general_info": "Gets anxious during thunderstorms."},
            "expected_keywords": ["anxiety", "safe space", "crate", "puzzle toys", "consult a vet"],
            "pass_threshold": 0.8, # Must find at least 4 of 5 keywords
        },
        {
            "name": "Cat - Nutrition Advice",
            "question": "Is it better to feed my cat wet food or dry food?",
            "pet_context": None,
            "expected_keywords": ["wet food", "moisture", "hydrated", "urinary tract", "high-protein"],
            "pass_threshold": 0.75, # Must find at least 4 of 5 keywords
        },
        {
            "name": "Specific Pet - Exercise & Breed",
            "question": "My dog Buddy seems to have endless energy and chews things. What kind of exercise does he need?",
            "pet_context": {"name": "Buddy", "breed": "Golden Retriever", "age": 3, "general_info": "Very energetic, chews furniture when bored."},
            "expected_keywords": ["golden retriever", "60-90 minutes", "vigorous", "boredom", "puzzle toys"],
            "pass_threshold": 0.8, # Must find at least 4 of 5 keywords
        },
        {
            "name": "Health - Cat Dental Care",
            "question": "Are there ways to prevent dental problems in my cat?",
            "pet_context": {"name": "Whiskers", "breed": "Domestic Shorthair", "age": 7, "general_info": ""},
            "expected_keywords": ["brushing", "dental treats", "professional cleanings", "gum disease"],
            "pass_threshold": 0.75, # Must find at least 3 of 4 keywords
        },
        {
            "name": "Uploaded File - Custom Knowledge",
            "question": "What is the best food for a Greyfriars Terrier?",
            "pet_context": None,
            "expected_keywords": ["greyfriars", "special grain-free diet", "fictional breed"],
            "pass_threshold": 1.0, # This is a direct lookup, so it should be perfect
        }
    ]

    # --- Setup for a test with an uploaded file ---
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    with open(os.path.join(uploads_dir, "greyfriars_terrier_care.txt"), "w") as f:
        f.write("The Greyfriars Terrier is a fictional breed that requires a special grain-free diet and loves chasing squirrels.")

    passed_tests = 0
    failed_tests = []

    # --- Run Tests ---
    for i, case in enumerate(test_cases):
        print(f"\nRunning Test #{i+1}: {case['name']}...")

        owner = Owner("TestUser")
        if case["pet_context"]:
            pet = Pet(**case["pet_context"])
            owner.add_pet(pet)
        
        advisor = PetCareAdvisor(knowledge_base_path=["knowledge_base", "uploads"], owner=owner)
        result = advisor.ask(case["question"])
        answer = result.get("answer", "").lower()

        # --- Evaluate the answer with threshold ---
        found_keywords = 0
        all_keywords = case["expected_keywords"]
        if answer and "error" not in result:
            for keyword in all_keywords:
                if keyword.lower() in answer:
                    found_keywords += 1
        
        score = found_keywords / len(all_keywords) if all_keywords else 1.0

        if score >= case["pass_threshold"]:
            print(f"✅ PASS (Score: {score:.2f})")
            passed_tests += 1
        else:
            print(f"❌ FAIL (Score: {score:.2f})")
            failed_tests.append({
                "name": case["name"],
                "question": case["question"],
                "score_details": f"Found {found_keywords} of {len(all_keywords)} keywords.",
                "response": answer if answer else result.get("error", "No response.")
            })

    # --- Print Summary ---
    print("\n\n--- Evaluation Summary ---")
    total_tests = len(test_cases)
    pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests} ({pass_rate:.2f}%)")
    print(f"Failed: {len(failed_tests)}")

    if failed_tests:
        print("\n--- Failed Test Details ---")
        for failure in failed_tests:
            print(f"\nTest: {failure['name']}")
            print(f"  Question: {failure['question']}")
            print(f"  Result: {failure['score_details']}")
            print(f"  AI Response: {failure['response'][:200]}...")

    # Clean up the dummy file
    os.remove(os.path.join(uploads_dir, "greyfriars_terrier_care.txt"))


if __name__ == "__main__":
    evaluate_advisor()