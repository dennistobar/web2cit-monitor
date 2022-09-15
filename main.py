import argparse
from monitor.prefix import Prefix

from writer.domain import DomainWriter


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Web2cit monitor runner")
    parser.add_argument('--domain', type=str,
                        help="Domain name (www.example.org)")
    parser.add_argument('--all', action='store_true',
                        help="Execute all domains from Meta")
    parser.add_argument('--log', action='store_true',
                        help="Writes in logs file and not in Meta (just debug in local mode)")
    parser.add_argument('--trigger', type=str, default="manual",
                        help="Explanation about invocation")
    return parser.parse_args()


def main():
    """Entry point for the main function"""
    args = parse_args()
    parameters = vars(args)

    if parameters.get('domain') is not None:
        writer = DomainWriter(domain=parameters.get('domain'),
                              log=parameters.get('log'),
                              trigger=parameters.get('trigger'))
        writer.write()
        return

    if parameters.get('all') is True:
        pf = Prefix()
        for domain_name in pf.run():
            writer = DomainWriter(domain=domain_name,
                                  log=parameters.get('log'),
                                  trigger=parameters.get('trigger'))
            writer.write()


if __name__ == '__main__':
    main()
