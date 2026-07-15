# Scenario
#Listen to this story: a boy and his father, a computer programmer, are playing with wooden blocks. They are building a pyramid.
#Their pyramid is a bit weird, as it is actually a pyramid-shaped wall – it's flat. The pyramid is stacked according to one simple principle: 
# each lower layer contains one block more than the layer above.
#Your task is to write a program which reads the number of blocks the builders have, and outputs the height of the pyramid that can be built using these blocks.
#Note: the height is measured by the number of fully completed layers – if the builders don't have a sufficient number of blocks and cannot complete the next layer, 
# they finish their work immediately.


blocks = int(input("Enter the number of blocks: "))

def calculate_pyramid_height(blocks):
    height = 0
    current_layer_requirement = 1

    # Loop runs as long as we have enough blocks to fully complete the next layer
    while blocks >= current_layer_requirement:
        blocks -= current_layer_requirement
        height += 1
        current_layer_requirement += 1  # The next layer needs one more block than the current one
    return height

height = calculate_pyramid_height(blocks)
print("The height of the pyramid:", height)



##### Other examples of print() function usage
print("The itsy bitsy spider" , "climbed up" , "the waterspout.")
print("My name is", "Python.", end=" ")
print("Monty Python.")
print("My", "name", "is", "Monty", "Python.", sep="-")
print("My", "name", "is", sep="_", end="*")
print("Monty", "Python.", sep="*", end="*\n")
print()


# Sample Solution
###################
print("original version:")
###################
print("    *")
print("   * *")
print("  *   *")
print(" *     *")
print("***   ***")
print("  *   *")
print("  *   *")
print("  *****")
###################
print("with fewer 'print()' invocations:")
###################
print("    *\n   * *\n  *   *\n *     *\n***   ***")
print("  *   *\n  *   *\n  *****")
###################
print("higher:")
###################
print("        *")
print("       * *")
print("      *   *")
print("     *     *")
print("    *       *")
print("   *         *")
print("  *           *")
print(" *             *")
print("******     ******")
print("     *     *")
print("     *     *")
print("     *     *")
print("     *     *")
print("     *     *")
print("     *     *")
print("     *******")
###################
print("doubled:")
###################
print("        *        "*2)
print("       * *       "*2)
print("      *   *      "*2)
print("     *     *     "*2)
print("    *       *    "*2)
print("   *         *   "*2)
print("  *           *  "*2)
print(" *             * "*2)
print("******     ******"*2)
print("     *     *     "*2)
print("     *     *     "*2)
print("     *     *     "*2)
print("     *     *     "*2)
print("     *     *     "*2)
print("     *     *     "*2)
print("     *******     "*2)

# print("Greg")
# print(Greg)
# print"Greg"
# print('Greg')
# print("Greg") print("Python")

hour = int(input("Starting time (hours): "))
mins = int(input("Starting time (minutes): "))
duration = int(input("Event duration (minutes): "))

mins += duration # find a total of all minutes
hour += mins // 60 # find a number of hours hidden in minutes and update the hour
mins %= 60 # correct minutes to fall in the (0..59) range
hour %= 24 # correct hours to fall in the (0..23) range
print(hour,mins, sep=":")
