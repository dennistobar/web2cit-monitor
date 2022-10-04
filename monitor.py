import argparse
from monitor.prefix import Prefix


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Web2cit monitor monitor to queue")
    parser.add_argument('--prefix', action="store_true",
                        help="Check all prefix")
    parser.add_argument('--hours', type=int,
                        help="Hours to be checked if there is a change")
    parser.add_argument('--trigger', type=str, default="manual",
                        help="Explanation about invocation")
    return parser.parse_args()


def main():
    """Entry point for the main function"""
    args = parse_args()
    parameters = vars(args)

    if parameters.get('prefix') is True:
        pf = Prefix()
        print(pf.check_changed(hours=parameters.get('hours', 1)))


if __name__ == '__main__':
    main()
