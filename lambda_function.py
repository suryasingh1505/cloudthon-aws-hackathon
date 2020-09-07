import requests
import json
import boto3

def TC1():
    url='http://3.128.160.151/'
    x = requests.get(url)
    if (x.status_code==200): 
        return "Result : Test case pass : Applciation is accessible "
    else : 
        return "Result : Test case Failed : Applciation is not accessible  , getting Error code {} ".format(x.status_code)

def TC2():
    url='http://3.128.160.151/registration'
    x = requests.get(url)
    if (x.status_code==200): 
        return "Result : Test case pass : Register functionality is accessible"
    else : 
        return "Result : Test case Failed : Register functionality is not accessible  , getting Error code {} ".format(x.status_code)

def TC3():  
    url='http://3.128.160.151/'
    x = requests.get(url)
    if (x.status_code==200): 
        return "Result : Test case pass : Applciation is Secure "
    else : 
        return "Result : Test case Failed : Applciation is not Secure  , getting Error code {} ".format(x.status_code)

def TC4():  
    login_data = {'username':'sujit','password':'dhamale'}
    url='http://3.128.160.151/'
    login_url="http://3.128.160.151/login"
    
    with requests.Session() as s:
        r=s.get(url)
        r=s.post(login_url,data=login_data)
        if (r.text.find("Welcome {}".format(login_data['username']))!= -1):
            return "Result : Test case pass : Login functionality is wokring "
        if(r.text.find("Wrong Credentials") != -1):
             return "Result : Test case Failed : Login functionality is not wokring "

def TC5():  
    login_data = {'username':'sujit','password':'dhamale'}
    url='http://3.128.160.151/'
    login_url="http://3.128.160.151/login"
    
    search_data={'query':'book'}
    search_url="http://3.128.160.151/search"
    
    with requests.Session() as s:
        r=s.get(url)
        r=s.post(login_url,data=login_data)
        r=s.post(search_url,data=search_data)
        if (r.text.find("Total book found: ") != -1):
            return "Result : Test case pass : Search functionality is wokring "
        if (r.text.find("No Result found for") != -1):
            return "Result : Test case Failed : Search functionality is not wokring "

        
def lambda_handler(event, context):
    print("Testing Started ...... ")
    s3 = boto3.client('s3')
    bucket ='testcaseresult'
    fileName ="result.json"
    
    result={}
    result["\nTC 1 : is application accessable ? "]=TC1()
    result["\n\nTC 2 : is Register functionality accessable ? "]=TC2()
    result["\n\nTC 3 : is application Secure ? "]=TC3()
    result["\n\nTC 4 : Check for login functionality  "]=TC4()
    result["\n\nTC 5 : Check for Search functionality  "]=TC5()
    
    print("Testing completed ...... ")
    
    uploadByteStream = bytes(json.dumps(result).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=fileName, Body=uploadByteStream)
    
    print("Data Saved in S3 ...... ")    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
            }
    

if __name__ == "__main__": main()
