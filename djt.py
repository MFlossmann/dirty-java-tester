#!/usr/bin/python

"""Dirty Java Tester

Test Java programs for the SoSe 2017 Course Advanced Programming (Java) of the Albert Ludwigs Universität Freiburg

Version: 1.1
Author: Michael Floßmann
Copyrighted under GPLv3 License"""

import os
import re
import subprocess as sp
from termcolor import colored

classes = {}
# scan week directory
for entry in os.scandir("./"):
    if not entry.is_file(): # check only directories
        dirs = os.listdir(entry.name)
        if 'testcases' in dirs and 'src' in dirs:
            print(entry.name, " has testcases/ and src/!")
            # get the name of the java class
            class_name = os.listdir(entry.name + "/src")
            classes[class_name[0]] = entry.name

for cls in classes.keys():
    print(cls + ":")
    # Collect the testfiles
    tests = []
    for entry in os.listdir(classes[cls] + "/testcases"):
        if entry.endswith(".stdin"):
            tests.append(entry)

    print("\tThere are " + str(len(tests)) + " tests.")

    # execute the tests
    for t in tests:
        test_path = str(classes[cls]) + "/testcases/"
        solution = t.replace("stdin", "stdout")
        print("\tRunning test " + re.findall(r'\d+', t)[0] + "...", end='')

        with open(test_path + t) as test_file:
            # execute java class with testfile as input
            with sp.Popen(["/usr/bin/java", str(cls + ".Main")],
                          stdin=test_file,
                          stdout=sp.PIPE,
                          universal_newlines=True) as proc:
                sol_file = open(test_path + t.replace("stdin", "stdout"),
                                "r")
                # compare solution to result
                solution = sol_file.read()
                result = proc.stdout.read()

                if(result == solution):
                    print("Passed!")
                else:
                    test_file.seek(0) # we need to reread the stdin file
                    print(colored("Test failed!",
                                  "red",
                                  attrs=['bold']) +
                          colored("\nWith stdin: \n", "yellow") +
                          test_file.read())
                    print(colored("Expected:\n", "yellow") +
                          solution)
                    print(colored("Got:\n", "yellow") + result)

                sol_file.close()
