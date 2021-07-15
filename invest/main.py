import argparse
#user input for margin of safety and beta
#input:  python3 main.py --margin_of_safety 0.10 --beta 0.2
parser = argparse.ArgumentParser(description="Specify margin of safety and beta threshold")
parser.add_argument("--margin_of_safety",type=float, default=0.10)
parser.add_argument("--beta",type=float, default=0.10)
args = parser.parse_args()
print(args.margin_of_safety, args.beta)





