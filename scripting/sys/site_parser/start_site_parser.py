from scripting.sys.site_parser.site_parser import SiteParser
import argparse

"""
This script is used to start the site_parser script. It takes two arguments:
    --site_name: the name of the site to be parsed
    --mode: the mode of the parser (placement or page)
"""

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse argument for site_parser script")
    arg_parser.add_argument("--site_name")
    arg_parser.add_argument("--mode")
    args = arg_parser.parse_args()
    site_parser = SiteParser(args.site_name, args.mode)
    site_parser.parse()