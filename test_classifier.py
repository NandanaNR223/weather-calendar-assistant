from main import classify_activity

test_events = [
    ("Morning Run", "outdoor"),
    ("Walk the dog", "outdoor"),
    ("Beach day", "outdoor"),
    ("Doctor Appointment", "indoor"),
    ("Study at library", "indoor"),
    ("Grocery Shopping", "errand"),
    ("Bank Visit", "errand"),
    ("Coffee with Sarah", "unknown"),
    ("Movie Night", "unknown"),
    ("Pick up medicine", "errand"),
    ("Dentist Visit", "indoor"),
    ("Therapy Session", "indoor"),
    ("Pick up prescription", "errand"),
    ("Jog around campus", "outdoor"),
    ("Lunch with coworkers", "unknown"),
    ("Dinner downtown", "unknown"),
    ("Yoga class", "indoor"),
    ("Trail hike", "outdoor"),
    ("Team meeting", "indoor"),
    ("Costco run", "errand"),
    ("Dog walk", "outdoor"),
    ("Vet appointment", "indoor")
]

correct = 0

for activity, expected in test_events:
    predicted = classify_activity(activity)

    print("\nActivity: ", activity)
    print("Expected: ", expected)
    print("Predicted: ", predicted)

    if predicted == expected:
        correct += 1

print("\nFinal Score:")
print(f"{correct}/{len(test_events)} correct")
