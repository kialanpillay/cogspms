import argparse

from gnn.training.regressor import train


def main():
    train(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='huber')
    parser.add_argument('--dataset', type=str, default='JSE_clean_truncated')
    parser.add_argument('--window_size', type=int, default=30)
    parser.add_argument('--horizon', type=int, default=1)
    parser.add_argument('--train_length', type=float, default=6)
    parser.add_argument('--valid_length', type=float, default=2)
    parser.add_argument('--test_length', type=float, default=2)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--norm_method', type=str, default='z_score')
    parser.add_argument('--epoch', type=int, default=50)
    parser.add_argument('--node', type=int, default=0)

    args = parser.parse_args()
    main()
