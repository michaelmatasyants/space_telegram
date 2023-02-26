import requests
import spacex_nasa_api
import os
import argparse
from datetime import datetime


def main():
    image_parser = argparse.ArgumentParser(
        description='''Program downloads natural color imagery of Earth which
                       was taken by NASA's Earth Polychromatic Imaging Camera
                       (EPIC). If no extension of image and path to save are
                       given they'll be chosen by default (extension = png,
                       windows path = C:\\Users\\Michael\\Desktop,
                       linux path = /home/user).'''
    )
    image_parser.add_argument("-p", "--path", default=os.path.expanduser("~"),
                              help="enter path to save the image")
    image_parser.add_argument("-x", "--extension", default='png',
                              help="enter extension for the image png or jpg")
    args = image_parser.parse_args()
    spacex_nasa_api.check_create_path(args.path)
    url = "https://api.nasa.gov/EPIC"
    data_gathering_url = f"{url}/api/natural"
    payload = {"api_key": f"{spacex_nasa_api.get_api_key()['nasa_api_key']}"}
    about_image_json = requests.get(data_gathering_url, params=payload).json()
    for i in range(len(about_image_json)):
        date_image = datetime.fromisoformat(
            about_image_json[i]['date']).strftime("%Y/%m/%d")
        name_image = f"{about_image_json[i]['image']}.{args.extension}"
        image_url = "{}/archive/natural/{}/{}/{}".format(
            url, date_image, args.extension, name_image)
        image_response = requests.get(image_url, params=payload)
        spacex_nasa_api.save_image(image_response.content,
                                   args.path, name_image)
        print("{} has been successfully downloaded to {}".format(name_image,
                                                                 args.path))


if __name__ == "__main__":
    print(main())
