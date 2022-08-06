import json

f = open('combined_weights_of_back_to_back_homers.txt', 'r')
f_str = f.read()
combined_weights_of_back_to_back_homers = json.loads(f_str)
heaviest_duo = ""
for duo in combined_weights_of_back_to_back_homers:
    if heaviest_duo == "":
        heaviest_duo = duo
    if combined_weights_of_back_to_back_homers[duo][0] > combined_weights_of_back_to_back_homers[heaviest_duo][0]:
        heaviest_duo = duo

print(heaviest_duo, combined_weights_of_back_to_back_homers[heaviest_duo])