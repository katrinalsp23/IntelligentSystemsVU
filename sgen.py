

for x in range(0,20,5):
    print("kb.add_clause(~PC{}, Q{}, K{}, T{}, A{})".format(x+4, x+3, x+2, x+1, x))
    print("kb.add_clause(PC{}, ~Q{}, ~K{}, ~T{}, ~A{})".format(x+4, x+3, x+2, x+1, x))
    # print("kb.add_clause(K{})".format(x+2, x+2))
    # print("kb.add_clause(Q{})".format(x+3, x+3))
    # print("kb.add_clause(J{})".format(x+4, x+4))

print("")

for x in range(0,20,5):
    print("kb.add_clause(~PC{}, K{}, T{}, A{})".format(x+3, x+2, x+1, x))
    print("kb.add_clause(PC{}, ~K{}, ~T{}, ~A{})".format(x+3, x+2, x+1, x))

print("")

for x in range(0,20,5):
    print("kb.add_clause(~PC{}, T{}, A{})".format(x+2, x+1, x))
    print("kb.add_clause(PC{}, ~T{}, ~A{})".format(x+2, x+1, x))

print("")

for x in range(0,20,5):
    print("kb.add_clause(~PC{}, A{})".format(x+1, x))
    print("kb.add_clause(PC{}, ~A{})".format(x+1, x))

print("")


