from scripting.sys.site_parser.site_parser import SiteParser
import argparse

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Parse argument for site_parser script")
    arg_parser.add_argument("--site_name")
    arg_parser.add_argument("--mode")
    args = arg_parser.parse_args()
    site_parser = SiteParser(args.site_name, args.parser_import_path, args.mode)
    site_parser.parse()