import re
import numpy as np

def main():
  with open("./brain", "r") as f:
    brain = f.read()
    brain = brain.replace("\n", " ").strip()
    #remove all space after [
    regex = r"\[\s+"
    brain = re.sub(regex, "[", brain)
    regex = r"(?<!\[)\s+"
    brain = re.sub(regex, ",", brain)

    brain_arrays = eval(brain)

    np_brain_w1 = np.array(brain_arrays[0])
    np_brain_w2 = np.array(brain_arrays[1])
    np_brain_w3 = np.array(brain_arrays[2])

    np.save("best_brain_restored/brain-w1", np_brain_w1)
    np.save("best_brain_restored/brain-w2", np_brain_w2)
    np.save("best_brain_restored/brain-w3", np_brain_w3)

main()