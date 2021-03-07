import sys
import argparse
import base64
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(asctime)s] - PID: %(process)d - TID: %(thread)d - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def log(s):
    logger.info(s)


def from_b64(input_, output):
    logger.info("Converting {} to {}...".format(input_, output))
    try:
        with open(input_, "r") as source:
            contents = base64.b64decode(source.read())
        with open(output, "wb") as destination:
            destination.write(contents)
    except Exception as e:
        logger.exception(e)
    else:
        log("{} created successfully.".format(output))


def to_b64(input_, output):
    try:
        with open(input_, "rb") as source:
            contents = base64.b64encode(source.read())
        with open(output, "wb") as destination:
            destination.write(contents)
    except Exception as e:
        logger.exception(e)
    else:
        log("{} created successfully.".format(output))


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-e", "--encode", action="store_true", help="Encode file")
        parser.add_argument("-d", "--decode", action="store_true", help="Decode file")
        parser.add_argument("-i", "--input", help="Input filename")
        parser.add_argument("-o", "--output", help="Output filename")
        args = parser.parse_args()

        if len(sys.argv) < 2:
            parser.print_help()
            sys.exit(1)

        if args.input and args.output:
            if args.decode:
                from_b64(args.input, args.output)
            elif args.encode:
                to_b64(args.input, args.output)
            else:
                logger.info("You need to specify (e)ncode or (d)ecode as parameter.")
        else:
            logger.info("You need to specify input and output.")

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
