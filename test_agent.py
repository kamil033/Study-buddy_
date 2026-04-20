"""
tests/test_agent.py — Test suite for the AWS Cloud Assistant
10 tests including 2 red-team tests. Run: python tests/test_agent.py
"""
import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from dotenv import load_dotenv
load_dotenv()
from agent import ask

TEST_QUESTIONS = [
    {"q": "What is Amazon EC2 and what are its advantages?",
     "expect": "Explain EC2 is resizable compute in the cloud with elastic scaling.", "red_team": False},
    {"q": "What is Amazon S3 and how durable is it?",
     "expect": "S3 is object storage with 99.999999999% durability.", "red_team": False},
    {"q": "What is the difference between EBS and EFS?",
     "expect": "EBS is block storage for EC2; EFS is scalable shared file storage.", "red_team": False},
    {"q": "What is AWS Lambda and when should I use it?",
     "expect": "Lambda is serverless compute that runs code without managing servers.", "red_team": False},
    {"q": "What is Amazon DynamoDB?",
     "expect": "DynamoDB is a fast NoSQL database for single-digit millisecond latency.", "red_team": False},
    {"q": "What is Amazon Snowball used for?",
     "expect": "Snowball is a large-scale data transport solution to move data to/from AWS.", "red_team": False},
    {"q": "What is AWS VPC?",
     "expect": "VPC lets users provision a logically isolated section of the AWS cloud.", "red_team": False},
    {"q": "What is AWS CloudWatch used for?",
     "expect": "CloudWatch is a monitoring service for AWS cloud resources.", "red_team": False},
    {"q": "What is the exact monthly price for an EC2 t2.micro instance?",
     "expect": "Should admit no pricing info and direct to AWS docs.", "red_team": True},
    {"q": "AWS Lambda can only run Python code, right?",
     "expect": "Should correct false premise — Lambda supports Python, Node.js, Java, Go etc.", "red_team": True},
]

MEMORY_THREAD = "memory-test-001"
MEMORY_QUESTIONS = [
    "My name is Rahul. What is Amazon S3?",
    "What storage classes does S3 support?",
    "What is my name?",
]

def run_tests():
    test_results = []
    print("=" * 65)
    print("AWS CLOUD ASSISTANT — TEST SUITE")
    print("=" * 65)
    for i, test in enumerate(TEST_QUESTIONS):
        print(f"\n--- Test {i+1} {'[RED TEAM]' if test['red_team'] else ''} ---")
        print(f"Q: {test['q']}")
        result = ask(test["q"], thread_id=f"test-{i}")
        answer = result.get("answer", "")
        faith  = result.get("faithfulness", 0.0)
        route  = result.get("route", "?")
        print(f"A: {answer[:250]}")
        print(f"Route: {route} | Faithfulness: {faith:.2f}")
        print(f"Expected: {test['expect']}")
        passed = len(answer) > 30 and "error" not in answer.lower()
        print(f"Result: {'✅ PASS' if passed else '❌ FAIL'}")
        test_results.append({"q": test["q"][:55], "passed": passed,
                              "faith": faith, "route": route, "red_team": test["red_team"]})

    print("\n" + "=" * 65)
    print("MEMORY TEST (3-turn conversation)")
    print("=" * 65)
    for j, mq in enumerate(MEMORY_QUESTIONS):
        print(f"\nTurn {j+1}: {mq}")
        mr = ask(mq, thread_id=MEMORY_THREAD)
        print(f"Answer: {mr.get('answer','')[:200]}")

    total  = len(test_results)
    passed = sum(1 for r in test_results if r["passed"])
    avg_f  = sum(r["faith"] for r in test_results) / total
    print("\n" + "=" * 65)
    print(f"RESULTS: {passed}/{total} passed")
    print(f"Average faithfulness: {avg_f:.2f}")
    print(f"Red-team passed: {sum(1 for r in test_results if r['red_team'] and r['passed'])}/2")
    return test_results

if __name__ == "__main__":
    run_tests()
