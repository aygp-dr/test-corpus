def append_lists(list1, list2):
    # Implementation with mutation bug
    # Bug: Modifies the input list instead of creating a new one
    list1.extend(list2)  # Mutates list1 instead of returning new list
    return list1

if __name__ == "__main__":
    # Test the function
    a = [1, 2, 3]
    b = [4, 5, 6]
    result = append_lists(a, b)
    print("Result:", result)
    print("Original list a (modified!):", a)  # Shows the bug