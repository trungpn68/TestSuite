import requests
import itertools
from copy import deepcopy
from concatnateImage import concatNimageAndText
import uuid
import os
import json
import argparse


def generateDynamicTestCases(staticParams, dynamicParams: dict):
    '''
    dynamicParams = {
        "style": ["anime", "lol", "naruto"],
        "strength": [0.1, 0.2]
    }
    '''
    combinations = itertools.product(*list(dynamicParams.values()))
    dictCombinations = []
    paramKeys = list(dynamicParams.keys())
    for combination in combinations:
        dynamicDict = {
            paramKeys[i]: combination[i] for i in range(paramKeys)
        }
        dynamicDict.update(staticParams)
        dictCombinations.append(dynamicDict)
    
    return dictCombinations

def testImages(url, inputImagesFolder, repeatPerRequest, requestJsonFile):
    '''
    Example:
    
    url = "localhost:8000/convert"
    repeatPerRequest = 3,
    headers = {
        ...sth
    }
    '''
    with open(requestJsonFile, "r") as file:
        requestInfo = json.loads(file.read())

    for imageName in os.listdir(inputImagesFolder):
        imagePath = os.path.join(inputImagesFolder, imageName)
        with open(imagePath, "rb") as imageFile:
            inputImage = imageFile.read()

        for style in requestInfo["styleEnum"]:
            os.makedirs(f"outputs/{style}", exist_ok=True)
            requestInfo['queryParams'].update({"style": style})
            for i in range(repeatPerRequest):
                response = requests.post(url=url, 
                                        files={ "file": (imageName, inputImage, f"image/{imageName.rsplit('.')[-1]}") }, 
                                        params=requestInfo['queryParams'])
                
                image_files = [inputImage]
                if 'json' in response.headers['content-type']:
                    print(response.json())
                elif 'image' in response.headers['content-type']:
                    print(f"{imageName}__{i}")
                    image_files.append(response.content)
                    concatNimageAndText(image_files, requestInfo, f"outputs/{style}/{imageName+'_'+style}__{i}.jpg")

# def requestImagesGenerate(url, paramData, queryParams, repeatPerRequest, headers=None):
#     '''
#     Example:
    
#     url = "localhost:8000/convert"
#     repeatPerRequest = 3,
#     headers = {
#         ...sth
#     }
#     '''
#     for params in paramData:
#         files = {}
#         newParams = deepcopy(params)
#         for key, value in params:
#             if value.startswith('file:'):
#                 with open(value[5:], "rb") as file:
#                     files[key] = file.read()
#                 newParams.pop(key) 

#         imageId = uuid.uuid4()
#         for i in range(repeatPerRequest):
#             response = requests.post(url=url, data=newParams, files=files, headers=headers, params=queryParams)
#             image_files = list(files.values())
#             if 'image' in response.headers['content-type']:
#                 image_files.append(response.content)
#                 concatNimageAndText(image_files, newParams, f"outputs/{imageId}__{i}")

# if __name__ == "__main__":
#     testImages("http://192.168.101.101:1234/convert", "/Users/engreed/Downloads/avatar_processed", 2, "requestInfo.json")

parser = argparse.ArgumentParser()
parser.add_argument("inputFolder")
parser.add_argument("-u", "--url")
parser.add_argument("-r", "--repeat")
parser.add_argument("-j", "--request-json")
args = parser.parse_args()

print(args.url)
testImages(args.url, args.inputFolder, int(args.repeat), args.request_json)

