# 1. Show how to set the complexity formula (parameters, weight)
# 2. How to set the thresholds among all the cases.
# 3. Show how many cases (in other word, the total number of benchmarks) are in each complexity interval
# 4. Use "LiteratureCases.input" to calculate metrics for top 15 cases from other papers
# (No need for a graphical representation)
# 5. Generate other different cases in each complexity interval except literature cases
# 6. Explain the metrics

# How many possible graphs can be generated in the first section [0, 30]
# max_value = 30
# PossibleGraphAmount = 0
# n = 1
# while n < 15:
#     m = 1
#     while m < 30:
#         if m > n*(n-1)/2:
#             break
#         else:
#             PossibleGraphAmount += 1
#         m += 1
#     n += 1
# print(PossibleGraphAmount)

# How many possible graphs can be generated in the first section [30, 100]
# max_value = 100
# PossibleGraphAmount = 0
# n = 15
# while n < 50:
#     m = 1
#     while m < 100:
#         if m > n*(n-1)/2:
#             break
#         else:
#             PossibleGraphAmount += 1
#         m += 1
#     n += 1
# print(PossibleGraphAmount)

# How many possible graphs can be generated in the first section [100, 500]
# max_value = 500
# PossibleGraphAmount = 0
# n = 50
# while n < 500:
#     m = 1
#     while m < 250:
#         if m > n*(n-1)/2:
#             break
#         else:
#             PossibleGraphAmount += 1
#         m += 1
#     n += 1
# print(PossibleGraphAmount)
