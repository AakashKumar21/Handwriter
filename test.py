from os import listdir


path = "images\\random_bg\\"

print(listdir(path))

background_entropy = 4

bg_parts = []
if background_entropy == 4:
    all_parts = listdir(path)
    for part in all_parts:
        if "cross_4" in part:
            bg_parts.append(part)

for f in bg_parts:
    print(f)