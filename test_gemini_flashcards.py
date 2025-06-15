import time
from gemini_utils import gemini_generate_flashcards

def test_all_categories():
    categories = ['General', 'Biology', 'History', 'Computer Science', 'Physics', 'Chemistry', 'Mathematics', 'Other']
    prompt = 'Explain how AI works in a few words'
    results = {}
    start = time.time()
    for cat in categories:
        try:
            t0 = time.time()
            result = gemini_generate_flashcards(prompt, cat)
            elapsed = time.time() - t0
            results[cat] = {'result': result[:200] + ('...' if len(result) > 200 else ''), 'time': round(elapsed, 2)}
        except Exception as e:
            results[cat] = {'error': str(e)}
    total = time.time() - start
    print(f"Tested {len(categories)} categories in {round(total, 2)}s.")
    for cat in categories:
        print(f"\n[{cat}] ({results[cat].get('time', 'error')}s):\n{results[cat].get('result', results[cat].get('error'))}")

if __name__ == '__main__':
    test_all_categories()
