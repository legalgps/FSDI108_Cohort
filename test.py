from data import data

categories = []
for item in data:
    cat = item["category"]

    if cat not in categories:
        categories.append(cat)

print(categories)


# def print_test2(limit):
#     for item in data:
#         if item["price"] > limit:
#             print(item["title"])


# # from file named data import variable named data
# # def test_forloop():
# #     for i in range(10):
# #         print(i)
# # def print_titles():
# #     for prod in data:
# #         print(prod["title"])
# for item in data:
#     results_list = item
#     print("results_list")


# def print_sum():

#     sum = 0
#     for item in data:
#         sum += item["price"]

#     print(f"The sum is:{sum}")


# def print_total_value():
#     sum = 0.0
#     for item in data:
#         sum += item["price"] * item["stock"]

#     print(f"Total Stock Value = {sum}")


# def print_test2(limit):
#     for item in data:
#         if item["price"] > limit:
#             print(item["title"])


# # for item in data:
# #     results_list = item
# #     print("results_list")

# # def print_categories_list():

# #     # def run_test():
# #     #     print("running tests")

# #     # test_forloop()
# #     # print_titles()
# #     print_sum()  # should print the sum of all prices in the catalog
# #     print_test2(10)
# #     print_total_value()

# print_categories_list()


# run_test()


# import data
# travel for loop for data
# print the object inside the data
